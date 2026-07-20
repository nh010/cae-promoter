# CAE Promoter — intake form field map (source of truth for pre-fill)

**Form:** CyberAgents Exchange: Contributor Promotion Intake Form
**Responder link:** https://forms.gle/f3Hsev3fp7XNpNCw6
**Canonical viewform:** https://docs.google.com/forms/d/e/1FAIpQLSf27i8jsPMbIwtp4FFHBd3F5RBHGXK-65ONDB7O0VHFMC16kw/viewform
**Pre-fill base:** append `?` + `&`-joined `entry.<id>=<url-encoded value>` to the viewform URL.
**Extracted:** 2026-07-20 (live re-extract, via Playwright reading `FB_PUBLIC_LOAD_DATA_`). 24 fields.

> **Changed 2026-07-20 (18 → 24 fields).** Added a six-field "social handles" block (a required
> social-tagging opt-in + five optional handle fields); moved Work email up to #2 and GitHub handle
> down into the socials block; added an "Other" option to Contributor type and Build type; refined
> several labels. All 18 prior `entry.<id>`s are unchanged.

## Field map (form order)

| # | Field | Type | Required | entry ID | Pre-fill source (skill session) |
|---|-------|------|----------|----------|----------------------------------|
| 1 | First and last name | Short answer | yes | `entry.1596500923` | contributor name |
| 2 | Work email | Short answer | yes | `entry.1580263152` | interview |
| 3 | Contributor type | Multiple choice | yes | `entry.1899964244` | interview (employee/partner/community) |
| 4 | Job title | Short answer | yes | `entry.34266064` | interview |
| 5 | Organization name | Short answer | yes | `entry.1135422228` | interview |
| 6 | Organization size (# of employees) | Short answer | yes | `entry.1236656087` | interview — specific #, else range ladder |
| 7 | Size of security team (# of FTEs on cyber team) | Short answer | yes | `entry.1678117250` | interview — specific #, else range ladder |
| 8 | Region | Multiple choice | yes | `entry.1880062348` | interview |
| 9 | Industry | Multiple choice | yes | `entry.1581560595` | interview |
| 10 | Name of agent/skill/etc. | Short answer | yes | `entry.1153617233` | listing name (ingest) |
| 11 | Build type | Multiple choice | yes | `entry.1563284810` | listing type (ingest) |
| 12 | Exchange listing URL | Short answer | yes | `entry.546272964` | ingest input |
| 13 | GitHub repo URL | Short answer | yes | `entry.80140529` | ingest input |
| 14 | Value statement #1 | Paragraph | yes | `entry.1167207484` | value-statements.md (primary) |
| 15 | Value statement #2 | Paragraph | no | `entry.1470473782` | value-statements.md |
| 16 | Value statement #3 | Paragraph | no | `entry.415351116` | value-statements.md |
| 17 | Social-tagging opt-in | Multiple choice | yes | `entry.1985420160` | interview (Yes/No) |
| 18 | X/Twitter handle | Short answer | no | `entry.1079612501` | interview (only if opted in) |
| 19 | Bluesky handle | Short answer | no | `entry.2085830831` | interview (only if opted in) |
| 20 | LinkedIn profile | Short answer | no | `entry.1615438749` | interview (only if opted in) |
| 21 | Reddit handle | Short answer | no | `entry.859295616` | interview (only if opted in) |
| 22 | GitHub handle | Short answer | no | `entry.1037521172` | derived from repo URL / interview |
| 23 | Other social media profile/handle | Short answer | no | `entry.1278806003` | interview (only if opted in) |
| 24 | Future outreach | Multiple choice | yes | `entry.963519517` | interview (Yes/No) |

## Exact option strings (multiple-choice pre-fill must match verbatim)

**Contributor type (`entry.1899964244`):** `Community contributor` · `Tenable employee` · `Tenable partner` — **also carries an "Other" free-text option** (see "Other" pre-fill below). The skill always knows the type, so it never needs "Other" here.

**Region (`entry.1880062348`):** `Asia-Pacific (incl. Australia and New Zealand)` · `Europe` · `Latin America (Mexico, Central, and South America)` · `North America (US, Canada)` · `Middle East and Africa` — **plus an "Other" free-text option.**

**Industry (`entry.1581560595`):** `Education` · `Financial institutions and insurance` · `Government and public sector` · `Healthcare and life sciences` · `Manufacturing and industrial` · `Retail and e-commerce` · `Technology and software` · `Telecommunications and media` — **plus an "Other" free-text option.**

**Build type (`entry.1563284810`):** `Agent` · `Skill` · `MCP Server` · `Playbook` — **now also carries an "Other" free-text option** (added 2026-07-20). The skill knows the listing type from ingest, so it never needs "Other" here.

**Social-tagging opt-in (`entry.1985420160`):** `Yes` · `No` — plus a stray "Other" free-text option on the form. The skill only ever sends `Yes` or `No`.

**Future outreach (`entry.963519517`):** `Yes` · `No` (no "Other").

## Size fields — specific-first, range fallback (open text)

Fields 6 and 7 are **open text**, required. The skill asks for a specific number first and
inserts it verbatim (e.g., `4200`, `7`). Only if the contributor declines to specify does the
skill insert one **fixed** range string (so the column stays consistent and a range is visually
self-identifying vs. a specific number):

- **Organization size (`entry.1236656087`):** `1–50` · `51–500` · `501–5,000` · `5,001–25,000` · `25,000+`
- **Security team size (`entry.1678117250`):** `1–10` · `11–50` · `51–200` · `201–500` · `500+`

Note field 7 is the **security team** headcount specifically (FTEs on the cyber team), not total org headcount.

## Social handles block (fields 17–23) — gated on the opt-in

Field 17 (`entry.1985420160`) is a required Yes/No: *"If Tenable promotes your AI asset on our
social media channels, would you like us to tag you in the post(s)?"* Fields 18–23 are the
handle fields it gates:

- If the contributor answers **Yes**, the skill collects whichever handles they use (X/Twitter,
  Bluesky, LinkedIn, Reddit, GitHub, or a free-text "Other") and pre-fills only those provided.
- If **No**, the skill sends `No` for field 17 and leaves the six handle fields empty.
- **GitHub handle (`entry.1037521172`)** is the one handle field the skill can often supply
  regardless — it's derivable from the repo URL — but it now lives in this block.
- All six handle fields are **optional**, so any not provided are simply omitted from the pre-fill
  (never sent as an empty `entry=` pair).

## "Other" pre-fill (Contributor type, Region, Industry, Build type, Social-tag opt-in)

These choice fields each carry a real **"Other" free-text** option (confirmed live: the option
list ends with an empty-label entry flagged `1` = Google's "Other" marker). To pre-fill "Other"
with a custom value, Google Forms needs **two** params, not one:

```
entry.<id>=__other_option__&entry.<id>.other_option_response=<url-encoded custom text>
```

So a contributor whose region/industry isn't listed still gets a clean pre-fill: the skill sends
`__other_option__` for the choice and their own words in the `.other_option_response` companion
param. This means the skill does **not** need to force an odd answer onto the nearest listed
option — prefer a listed option on an exact match, else use "Other" + their text.

In practice the skill only *needs* the "Other" mechanism for **Region** and **Industry**
(free-form demographics). Contributor type and Build type technically expose "Other" now, but the
skill always holds a known, listed value for both (from interview and ingest respectively), so it
should always emit the plain listed option there and treat an unmatched value as a bug, not an
"Other."

## Notes / gotchas
- Multiple-choice/dropdown pre-fill selects a **listed** option only on an exact string match
  (case, punctuation, parens, en dashes). For anything not on the list, use the "Other" mechanism
  above — never send unmatched free text to the plain `entry.<id>` param, or the field stays blank.
- **Future outreach** and **Future/social opt-in** are two different required fields now:
  `entry.963519517` (future research outreach, no "Other") vs. `entry.1985420160` (social-tagging
  opt-in that gates the handles block, has "Other"). Don't conflate them.
- Asset-identity fields (10–13) are not free text to elicit: the skill already holds all four from
  preflight + ingest, so they pre-fill cleanly.
- All required choice fields would block the contributor's submit on an unmatched-and-not-"Other"
  value — hence exact option strings matter.
