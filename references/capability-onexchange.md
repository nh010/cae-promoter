# Capability C — on-Exchange optimization

The leaderboard is the optimization target, so optimize for what actually moves it.

## Leaderboard mechanics (the actionable lever)

- **Rank = raw GitHub stars**, tie-broken by `rising`, then `pushedAt`.
- **Rising 🚀 = top 20% by stars-per-day among listings ≤ 90 days old.**
- So for a fresh listing, **early star *velocity*** is the lever — front-load promotion in the first
  weeks while the ≤90-day window and stars/day both count most.

## Concrete listing / README edits

- Sharper **dek** (≤30 words) and stronger **"What it does."**
- Correct **`integrations[]` and tags** from the **live controlled vocab** (`scripts/read_vocab.py`)
  — never hand-typed; use only validator-accepted values.
- Weave the **value statements** into the listing/README.
- Set the **`works_with_hexa` flag / badge only where the repo confirmed it** (see
  `guardrail-gates.md`).
- Improve README quality against Exchange norms (purpose, prereqs, how-to-run, outputs, limitations).

## The listing PR

On approval, help the contributor open a PR against `tenable/cyberagents-exchange` from **their own**
GitHub account. Mechanics live in `references/listing-pr.md` (cae-promoter's own standalone flow —
no submitter-skill dependency). This step decides **when** to offer it and **what** to change:
promo section + value statements + verified badge.

## Video-on-listing (external dependency)

The listing schema has **no video field today** (verified in `validator.py`). So the current
on-Exchange advice for video is: **link the demo from your README.** Adding a `video_url` field is
Exchange platform work this project doesn't own.
