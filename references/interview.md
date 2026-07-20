# Interview — preflight + up-front interview (session steps 0–2)

Five jobs, in order. This file is the source the metadata-truth gate points to.

## (a) Preflight — a published listing is required

Confirm the given URL resolves to a real listing and that it is **not** a seeded example
(`visibility: "example"`, e.g. `aristaeus-threat-to-board`). If there's no listing or only a seed,
**stop and refer the contributor to the `cyberagents-exchange-submit` skill** ("get listed, then
get promoted"). Do not fabricate a listing or a PR number, and do not proceed.

## (b) Identify + profile (derive-first, ask-only-the-gaps)

Ask contributor type → select the matching profile in `voice-profiles.md`. Then assemble the
**intake-form profile** by filling every field the skill can already determine *before asking
anything*:

- **Derive and offer for a one-tap confirm:** name, GitHub handle, organization, and often job
  title — from the listing `author`/`github_url` + the repo profile/README.
- **Ask only the non-derivable fields:** work email, region, industry, organization size,
  security-team size — plus **future-outreach consent** (always asked; it's a permission, never
  inferred).
- **Map region + industry to the intake form's fixed options** (see `docs/intake-form-fields.md`);
  the two sizes ask for a **specific number first**, falling back to one fixed range string only if
  the contributor declines.
- **Bar:** never ask for what could be derived; batch the true unknowns into as few prompts as
  possible. Record each field as **derived** vs. **asked** in the promo record.
- **When a "derivable" field isn't there:** job title and organization are *often* derivable but not
  always (many repos have neither, and `author` may be a placeholder like `Your Name`). If you can't
  derive one, **ask for it** — fold it into the same batch of gaps rather than leaving it blank.
  Both are **required** on the intake form, so an unfilled one blocks the contributor's submit; if
  the contributor genuinely can't/won't provide it, leave the pre-fill param out and flag
  `profile-gap` so it's visible rather than silently missing. Never invent a title or org.

## (c) The guided value-statement probe

The core of the interview — a four-move flow, not an open-ended "got metrics?":

1. **Present the five value categories** and ask the contributor to pick the **2–3** that best fit
   their tool, plus an **"Other — please specify"** option:
   1. **Operational efficiency** — e.g. "reduced investigation time from 45 min to 8 min"
   2. **Risk reduction** — e.g. "reduced exploitable critical exposures by 72%"
   3. **Faster response** — e.g. "reduced MTTR by 88%"
   4. **Better decisions** — e.g. "false positives dropped 65% while detection coverage increased"
   5. **Scale without headcount** — e.g. "existing team now manages 3x more assets, no added analysts"
2. **Propose three statements** aligned to the selected categories, drafted from the skill's
   analysis of the **listing + repo** (grounded in what the tool actually does, not generic).
3. **Contributor reviews and shapes them** — adjusts the numbers/estimates, requests revisions, or
   swaps one in. This is where each statement's **truth-status** is set: `measured` / `estimate` /
   `qualitative`. **No-metric path:** when there's no measured number, walk them from what they *do*
   know to a **defensible estimate** (e.g. "replaced a ~2-hr daily manual task → ~10 hrs/week"),
   record the reasoning, mark it `estimate`; degrade to `qualitative` only if even that's
   impossible. Never block for lack of a hard number, never inflate one (`unverified` flag if the
   truth-check can't substantiate a claim).
4. **Vary the framing** — deliberately vary sentence structure across the 2–3 statements (lead with
   the number / the outcome / the before→after) so listings don't read as boilerplate.

Write the shaped 2–3 statements to `promo/value-statements.md` (each with category + truth-status).
Voice/attribution applies — tune the "we/our" phrasing per contributor type.

## (d) Hexa AI detection + Tenable pull-through

Ask if it uses the Hexa AI MCP, then **verify against the repo code/docs before trusting a "yes"**
(same approach as the submitter skill, reimplemented here). Set no `works_with_hexa` flag or badge
without repo evidence. Also surface any Tenable-product-pull-through angle.

## (e) Social-tagging opt-in + handles (form fields 17–23)

The intake form added a required social-tagging opt-in (field 17, `entry.1985420160`) that gates
six handle fields. Handle this near the end of the interview, once rapport is established:

1. **Ask the opt-in:** "If Tenable promotes your asset on our social channels, want us to tag you?"
   (Yes / No.) This is required on the form — always capture it.
2. **If No:** send `No`; leave all six handle fields empty; move on.
3. **If Yes:** collect whichever handles the contributor actually uses — **X/Twitter, Bluesky,
   LinkedIn, Reddit, GitHub, and a free-text "Other social."** All six are optional; pre-fill only
   the ones provided, omit the rest. **GitHub handle** may already be derived from the repo URL
   (job b), so offer it for a one-tap confirm rather than re-asking — but **only supply it when the
   opt-in is Yes** (on No it stays empty like the other five; the opt-in gates all six handle
   fields, GitHub included).

Record the opt-in + provided handles under `socials` in the promo record.

## Submission PR number

Resolved in ingest via `scripts/find_pr.py` (fallback: ask the contributor to paste it). Required
for the promo clip (capability B). Don't invent it; if unresolved, the clip script carries a
`#TODO — paste your PR number` placeholder.
