---
name: cae-promoter
description: Use when any CyberAgents Exchange contributor (community, partner, or Tenable employee) wants to promote, market, or drive stars and installs to an already-published agent, skill, MCP server, or playbook — on the Exchange (Rising 🚀, leaderboard) or externally. Open to every contributor, community-first. Requires a published listing; refer unlisted contributors to cyberagents-exchange-submit first. Not for building or submitting an asset, and not for acting as Tenable.
---

# CAE Promoter

Coach **any** CyberAgents Exchange contributor — community, partner, or Tenable employee, and
**community-first** by design — to promote an **already-published** asset: interview for
quantifiable value, look up their submission PR, draft an on-brand `promo/` bundle, build a
pre-filled intake-form link they submit, prep them to record a promo clip and demo at a virtual
recording studio, and optionally open a listing-edit PR on their own GitHub. **It coaches and
drafts — it holds no Tenable credentials, posts nothing, and never acts as Tenable.** Its only
outputs are local files under `promo/` plus on-screen guidance. The promo package is the
contributor's to post on their own channels; Tenable also scouts standout contributions to amplify.

## Platform

Targets **Claude Code** (runs the Python helpers in `scripts/`). A contributor on **Claude Desktop
/ Cowork** should use the Desktop variant (a deferred fast-follow); until it ships, this skill still
works via the Claude-native fallbacks below — slower, without the deterministic scripts.

## Session spine

**Step 0 — Preflight (published listing required).** Run `scripts/fetch_listing.py <url>` — it exits
`NOT_FOUND` (no such listing) or `EXAMPLE_SEED` (`visibility: "example"`) instead of erroring; on
either, **stop and refer the contributor to the `cyberagents-exchange-submit` skill** ("get listed,
then get promoted"). If the URL 404s, the listing type in the URL may be wrong (e.g. a playbook seed
under `/agents/`) — re-check the type before concluding it doesn't exist. Do not fabricate a listing
or PR number. (Programmatic callers: `resolve_listing()` returns `None` for not-found and the dict
otherwise; `is_example(dict)` flags the seed.) See `references/interview.md` (job a).

**Step 1 — Ingest.** Ask for the Exchange listing URL + GitHub repo URL. Run
`scripts/fetch_listing.py <url>` for listing metadata; run `scripts/find_pr.py "<name>" <slug>` for
the **accepted submission PR number**. Deep-read the repo README/config for substance and
claim-verification (dispatch a subagent for a large repo). Load `scripts/read_vocab.py` (live
controlled vocab) and `references/capability-onexchange.md` (leaderboard mechanics).

**Step 2 — Interview / identify.** Follow `references/interview.md`: ask contributor type → load the
profile from `references/voice-profiles.md`; assemble the intake-form profile **derive-first** (ask
only the gaps + consent); run the **guided five-category value probe** → write
`promo/value-statements.md`; **detect + truth-check Hexa AI MCP** against the repo; capture the
**social-tagging opt-in + handles** (form field 17 gating six handle fields).

**Step 3 — Menu.** Offer capabilities A (copy), B (video), C (on-Exchange + listing PR), D (visual
aids); the contributor picks one or more. Each how-to is in its `references/capability-*.md`.
**Capability → scaffold token:** A → `copy`, B → `video`, D → `visual-aids`. **C has no scaffold
token** — it writes no distinct bundle files; it's realized through `copy/listing-section.md` (from
A) plus the listing-PR offer at handoff (Step 6). So only pass `copy`/`video`/`visual-aids` to
`scaffold_promo.py`; never pass `on-exchange` (it's silently dropped). If the contributor picks C
alone, still scaffold `copy` so `listing-section.md` exists.

**Step 4 — Emit.** Run `scripts/scaffold_promo.py <repo_root> <caps...>` to create `promo/`, then
fill each file per its reference, leading with the value statements and applying the three gates to
every string. The promo-clip script (B) embeds the PR number from Step 1. **Before finalizing each
copy file, run `scripts/brand_check.py <channel> <file>`** (channel ∈ x/linkedin/slack/listing) —
it deterministically catches straight quotes, the short-form one-em-dash cap, the X 280-char limit,
banned abbreviations, and banned phrases. Fix every finding; it exits non-zero until clean. This is
the mechanical half of Gate 3 (judgment calls — voice, customer names — still apply).

**Step 5 — Intake form.** After value statements are confirmed and the bundle is emitted, **before**
recording: follow `references/intake-form.md` → build the pre-filled link via
`scripts/build_prefill_url.py` → hand it over for the contributor to **review and submit themselves
(never auto-POST)** → record offered/submitted/declined. Submitting the form is also what triggers
Tenable to email the contributor their virtual recording studio link (Step 6). Declining does not
block the session.

**Step 6 — Approve & hand off.** Follow `references/handoff.md`: consent screen → explicit approval
→ set recording expectations — **once the contributor submits the intake form (Step 5), Tenable
emails them a virtual recording studio link**; the skill preps them with the promo-clip script + demo
outline in `promo/video/recording-outline.md` so they're ready when the link arrives → optionally
open the **promotion-edit PR** via `references/listing-pr.md` (contributor's own auth) → write
`promo/handoff.yaml`. Declining leaves everything local, writes no manifest, opens no PR.

## The three gates (always on)

Depth in `references/guardrail-gates.md`. Apply all three to every generated string:

1. **Metadata-truth (generative):** probe for firsthand quantifiable value; flag unverified metrics;
   no invented integrations vs. the listing's `integrations[]`; **verify `works_with_hexa` against
   the repo before any Hexa AI badge** (a "yes" is unproven until the code confirms it).
2. **Voice/attribution:** apply the contributor-type profile (`references/voice-profiles.md`) — get
   "who is *we*?" right; never imply the contributor is Tenable or that Tenable endorses the asset.
3. **Brand + legal:** run `scripts/brand_check.py` on every copy string for the mechanical checks
   (straight quotes, em-dash cap, X length, banned abbreviations/phrases), then apply
   `references/brand-rules.md` for the rest; flag customer names, third-party citations
   (Gartner/IDC/Forrester), and competitor UI to `review_flags`. **The skill flags; humans adjudicate.**

**Hard-stop refuse list (no bundle produced):** offensive/weaponized agents, hardcoded secrets,
undisclosed outbound calls, competitor targeting, weakening security controls.

## Script fallbacks (Claude-native, first-class for the Desktop lift)

Python scripts are the fast path, **not** a hard dependency. When Python/network is unavailable:

- **fetch_listing** — fetch the content-repo `<type>/<slug>.md` directly and parse its frontmatter.
- **find_pr** — run the GitHub search via `gh`/web, or ask the contributor to paste the PR number.
- **read_vocab** — read `validator.py` from the content repo and pull the `Literal[...]` enums.
- **scaffold_promo** — create the `promo/` tree with the file tools from `assets/` templates.
- **build_prefill_url** — assemble the `entry.<id>=<value>` query string inline from
  `docs/intake-form-fields.md` (the source-of-truth field map).
- **brand_check** — apply the `references/brand-rules.md` checklist by hand: straight→smart quotes,
  ≤1 em dash per short-form post, X ≤280 chars, no banned abbreviations/phrases.
