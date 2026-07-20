# Intake form — pre-filled link procedure (session step 5)

Runs **after** the value statements are confirmed and the bundle is emitted, **before** recording.
The skill builds a pre-filled Google Form link; the contributor reviews and submits it themselves.
**No auto-POST, no Tenable credential, no Forms API at runtime.**

**The entry-ID map, exact option strings, size range ladders, and viewform base URL live in
`docs/intake-form-fields.md` (source of truth, re-extracted live 2026-07-20, 24 fields).** Prefer
`scripts/build_prefill_url.py` to assemble the link deterministically; the Claude-native fallback
assembles it inline for the Desktop variant.

## Procedure

1. **Assemble the field→value map** from the profile (interview job b), the asset identity
   (preflight + ingest), `promo/value-statements.md`, and the socials opt-in + handles (interview
   job e).
2. **Validate the required choice fields against their listed options:**
   - **contributor_type, build_type** — the skill always holds a known value (type from interview,
     build from ingest), so these map to an exact listed option. An unmatched value here is a skill
     bug, not an "Other" case — `build_prefill_url.py` raises rather than guessing.
   - **region, industry** — free-form demographics. Prefer a listed option on an exact match; for an
     off-list answer ("we're global," an industry not listed) use Google's **two-param "Other"**
     mechanism (`entry.<id>=__other_option__` + `entry.<id>.other_option_response=<their words>`)
     rather than forcing the nearest option or sending unmatched text the field would ignore.
     Confirm the value with the contributor.
   - **social_tag_optin, future_outreach** — Yes/No; the skill only ever sends one of those.
3. **Sizes:** insert the specific number if given, else one fixed range string (ladders in the doc).
4. **Socials:** include handle fields only if the contributor opted in (Yes); omit any not provided.
5. **URL-encode** each value and append `entry.<id>=<value>` pairs to the viewform base (the script
   does this; `quote_plus`).
6. **Hand over the link:** "Review every pre-filled field, then click Submit." The skill never
   submits.
7. **Record the outcome** — offered / submitted / declined — in the promo record. Declining does
   **not** block the session.

## Why pre-fill, not auto-submit

The pre-fill only saves the contributor typing. Nothing reaches the team until they review and
click Submit on their own — the intake form is the single point where their details reach Tenable,
and it stays their action.
