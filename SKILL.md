---
name: outreach-drafts
description: This skill should be used when the user asks to "write outreach", "draft cold messages for these leads", "personalize an email or WhatsApp message", "write a cold call script", or wants first-touch messages for businesses from a leads list.
---

# Outreach Drafts

Write short, personalized first-touch messages for qualified leads. Draft only; never send anything.

## Workflow

1. **Gather inputs.** Need: what the user sells, the channel (email, WhatsApp, call script), their name and business, and a call to action (reply, short call, free audit). Ask once for anything missing.
2. **Personalize from CSV facts only**: business name, category, area, rating, review count, missing website. Never claim to have seen things not in the data (no "I checked your site" when there is no website field to base it on).
3. **Write per channel:**
   - Email: subject line under 8 words, body under 90 words, one clear ask.
   - WhatsApp or SMS: under 60 words, conversational, no attachments.
   - Call script: 15-second opener, one discovery question, one soft close.
4. **Draft for the top leads first** (priority A), then a reusable template with merge fields for the rest. Save to `outreach_drafts.md` or add a `message` column to the scored CSV.
5. **Offer variants** (direct vs. curious tone) when the user is unsure.

## Compliance reminders

Include a note with each batch:
- Identify the sender honestly and include an easy opt-out.
- Email: follow CAN-SPAM, GDPR or local equivalents. Calls and SMS in India: respect DND/TRAI rules and the DPDP Act. Check local rules for other regions.
- Do not use fake urgency, fake reviews or misleading claims about the recipient.
