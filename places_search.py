#!/usr/bin/env python3
"""Search the Google Places API (New) and export business leads to CSV.

Uses only the Python standard library. Requires the GOOGLE_MAPS_API_KEY
environment variable (Places API (New) must be enabled on the project).

Example:
    python places_search.py "dentists in Patna, Bihar" --max-results 40 \
        --no-website --out leads.csv
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

ENDPOINT = "https://places.googleapis.com/v1/places:searchText"
FIELD_MASK = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.primaryTypeDisplayName",
        "places.formattedAddress",
        "places.nationalPhoneNumber",
        "places.websiteUri",
        "places.rating",
        "places.userRatingCount",
        "places.businessStatus",
        "places.googleMapsUri",
        "nextPageToken",
    ]
)
COLUMNS = [
    "name",
    "category",
    "address",
    "phone",
    "website",
    "rating",
    "reviews",
    "status",
    "maps_url",
    "place_id",
]
API_MAX_RESULTS = 60  # Text Search returns at most 3 pages of 20


def build_payload(query, page_size, page_token=None, region=None,
                  language=None, min_rating=None, open_now=False):
    payload = {"textQuery": query, "pageSize": page_size}
    if page_token:
        payload["pageToken"] = page_token
    if region:
        payload["regionCode"] = region
    if language:
        payload["languageCode"] = language
    if min_rating is not None:
        payload["minRating"] = min_rating
    if open_now:
        payload["openNow"] = True
    return payload


def call_api(api_key, payload):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": FIELD_MASK,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        sys.exit(f"Places API error {exc.code}: {body}")
    except urllib.error.URLError as exc:
        sys.exit(f"Network error: {exc.reason}")


def flatten(place):
    return {
        "name": (place.get("displayName") or {}).get("text", ""),
        "category": (place.get("primaryTypeDisplayName") or {}).get("text", ""),
        "address": place.get("formattedAddress", ""),
        "phone": place.get("nationalPhoneNumber", ""),
        "website": place.get("websiteUri", ""),
        "rating": place.get("rating", ""),
        "reviews": place.get("userRatingCount", ""),
        "status": place.get("businessStatus", ""),
        "maps_url": place.get("googleMapsUri", ""),
        "place_id": place.get("id", ""),
    }


def keep(row, args):
    if row["status"] and row["status"] != "OPERATIONAL":
        return False
    if args.no_website and row["website"]:
        return False
    if args.require_website and not row["website"]:
        return False
    if args.require_phone and not row["phone"]:
        return False
    return True


def collect(api_key, args):
    rows, seen, token = [], set(), None
    target = min(args.max_results, API_MAX_RESULTS)
    while True:
        payload = build_payload(
            args.query, 20, token, args.region, args.language,
            args.min_rating, args.open_now,
        )
        data = call_api(api_key, payload)
        for place in data.get("places", []):
            row = flatten(place)
            if row["place_id"] in seen:
                continue
            seen.add(row["place_id"])
            if keep(row, args):
                rows.append(row)
        token = data.get("nextPageToken")
        if not token or len(seen) >= target:
            break
        time.sleep(2)  # next-page tokens take a moment to become valid
    return rows[: args.max_results]


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Export Google Places results to CSV.")
    p.add_argument("query", help='e.g. "plumbers in Austin, TX"')
    p.add_argument("--max-results", type=int, default=40,
                   help="Max leads to keep (API caps a query at 60). Default 40.")
    p.add_argument("--out", default="leads.csv", help="Output CSV path.")
    p.add_argument("--region", help="Region code bias, e.g. IN, US.")
    p.add_argument("--language", help="Language code, e.g. en, hi.")
    p.add_argument("--min-rating", type=float, help="Minimum rating, 0-5.")
    p.add_argument("--open-now", action="store_true", help="Only places open now.")
    p.add_argument("--no-website", action="store_true",
                   help="Keep only businesses with no website listed.")
    p.add_argument("--require-website", action="store_true",
                   help="Keep only businesses that have a website.")
    p.add_argument("--require-phone", action="store_true",
                   help="Keep only businesses with a phone number.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the request payload and exit without calling the API.")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.no_website and args.require_website:
        sys.exit("--no-website and --require-website cannot be combined.")
    if args.dry_run:
        print(json.dumps(
            build_payload(args.query, 20, None, args.region, args.language,
                          args.min_rating, args.open_now), indent=2))
        return
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        sys.exit("Set GOOGLE_MAPS_API_KEY (see .env.example / README).")
    rows = collect(api_key, args)
    write_csv(rows, args.out)
    print(f"Saved {len(rows)} leads to {args.out}")


if __name__ == "__main__":
    main()
