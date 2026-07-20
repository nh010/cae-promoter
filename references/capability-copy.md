# Capability A — written promo copy

Per-channel copy recipes. **Every draft leads with a value statement from
`promo/value-statements.md`** — the firsthand result, not features. Apply the three gates
(`guardrail-gates.md`) and the brand checklist (`brand-rules.md`) to every string, and the
contributor-type voice (`voice-profiles.md`). One CTA per piece. Cross-references the
`assets/copy/*.md` skeletons.

**Before you finalize any file here, run `scripts/brand_check.py <channel> <file>`** (channel ∈
x/linkedin/slack/listing). It's the deterministic mechanical gate — straight→smart quotes, the
short-form one-em-dash cap, the X 280-char limit, banned abbreviations, banned phrases — and exits
non-zero until clean. It catches exactly the failures easiest to miss by eye (a straight quote, a
281-char X post). Fix every finding, then apply the judgment-call rules below. (It ignores
`<!-- ... -->` template comments, so it's safe to run on a partly-filled file — it only checks the
real, contributor-visible copy.)

## LinkedIn (`copy/linkedin.md`)

A few short paragraphs. Hook (the result or the problem it kills) → one sentence on what the asset
does → the firsthand metric, attributable to the contributor → one CTA (listing link) → 3–5
lowercase hashtags. Sentence case, contractions OK, **≤1 em dash.**

## X / Twitter (`copy/x.md`)

**≤280 characters including the link.** Lead with the number; one clause on what it does; one link;
1–3 lowercase hashtags. **≤1 em dash.**

## Slack (`copy/slack.md`)

Plainspoken internal/community blurb, a couple of skimmable sentences, one link. Lead with the
result. **≤1 em dash.**

## Listing / README section (`copy/listing-section.md`)

The on-Exchange copy that helps win stars: a sharpened **dek** (≤30 words) → **"What it does"**
(2–4 plainspoken sentences) → **"The value we've seen"** (the truth-checked result, framed as the
contributor's own team's outcome; label estimates as estimates) → one CTA. Sentence-case headings;
hyperlink any stat/claim. This is longer-form, so minimize em dashes rather than counting them.

## Recording-studio auto-copy (note)

After recording, the virtual recording studio may auto-suggest social/blog/newsletter copy the
**team** can lift. That's a post-recording complement; the skill's brand-checked copy governs the
written bundle here.
