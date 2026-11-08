# Google Maps Lead Gen (Claude plugin)

Find local business leads with the **official Google Places API**, score them against your offer, and draft personalized outreach, all from Claude.

## What's inside

| Skill | What it does |
|-------|--------------|
| `maps-lead-search` | Searches Google Places for "business type in location", filters (no website, has phone, min rating) and exports a CSV |
| `lead-qualification` | Scores and ranks the CSV (A/B/C priority) based on what you sell |
| `outreach-drafts` | Writes email, WhatsApp or call-script first touches from the lead data |

`scripts/places_search.py` is a dependency-free Python script (standard library only) that the search skill runs.

## Setup

1. In Google Cloud, create a project, enable **Places API (New)** and create an API key. Restrict the key to that API.
2. Export the key:
   ```bash
   export GOOGLE_MAPS_API_KEY="your-key"
   ```
   (see `.env.example`; never commit real keys).
3. Install the plugin (see below).

## Install from GitHub

```bash
# Claude Code
/plugin marketplace add <your-github-username>/google-maps-lead-gen
/plugin install google-maps-lead-gen@google-maps-lead-gen-marketplace
```

For Claude Cowork / Claude desktop, upload the packaged `.plugin` file instead.

## Use

Ask Claude things like:

- "Find 40 dentists in Patna with a phone number but no website."
- "Score these leads for a website design offer."
- "Draft WhatsApp first messages for the A-priority leads."

Run the script directly:

```bash
python3 scripts/places_search.py "gyms in Pune" --max-results 40 --require-phone --out leads.csv
python3 scripts/places_search.py "gyms in Pune" --dry-run   # prints the request, no API call
```

## Publish to GitHub

```bash
cd google-maps-lead-gen
git init && git add . && git commit -m "Initial commit"
gh repo create google-maps-lead-gen --public --source=. --push
```

## Notes and limits

- One query returns at most 60 places (API limit). Split large areas into neighbourhoods.
- Places API usage is billed by Google; check current pricing and your free quota.
- Google's terms restrict caching and storing Places content. Use exports for active outreach and re-query rather than hoarding data.
- Outreach must follow CAN-SPAM/GDPR/DND/DPDP or your local rules. The plugin drafts messages and never sends them.

## License

MIT
