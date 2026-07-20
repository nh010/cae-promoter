# CAE Promoter

A Claude Code skill (Exchange-hosted) that coaches CyberAgents Exchange contributors to promote
their published AI assets. The skill name is **CAE Promoter**; the folder, slug, and invocation use
the lowercase-dashed form `cae-promoter`.

Its users are other contributors. It coaches and drafts — it holds no Tenable credentials, posts
nothing, and never acts as Tenable. Its only outputs are local files under `promo/` plus on-screen
guidance.

## Prerequisites

- **Claude Code** (this is a Claude Code skill; a Claude Desktop / Cowork variant is a fast-follow).
- **Python 3.10+** for the helper scripts (`scripts/`). They're the fast path, not a hard
  dependency — each has a Claude-native fallback, so the skill still runs without Python, just more
  slowly.
- **An already-published CyberAgents Exchange listing** for the asset you want to promote. Not
  listed yet? Use `cyberagents-exchange-submit` first.
- Optional: the **`gh` CLI** (authenticated as *you*) to look up your submission PR number and to
  open the optional listing-edit PR on your own account.

## How to use

1. Install the skill and run `/cae-promoter` in Claude Code.
2. Paste your **Exchange listing URL** and **GitHub repo URL** (the asset must already be published;
   if it isn't, use `cyberagents-exchange-submit` first).
3. Answer the short interview — contributor type, a few profile fields, and the **guided
   value-statement probe** (pick 2–3 value categories; the skill proposes statements from your
   listing + repo for you to shape).
4. Pick the capabilities you want: **A** promo copy, **B** video (Riverside), **C** on-Exchange
   optimization + listing PR, **D** visual aids.
5. Review the `promo/` bundle written into your repo (you own every word and every claim).
6. **Submit the pre-filled intake form** the skill hands you — review each field, then click Submit
   (the skill never submits for you).
7. **Record** the 30–60s promo clip and 2–3 min demo through the shared Riverside link, using
   `promo/video/recording-outline.md`.
8. Optionally open the **listing-edit PR** on your own GitHub, then hand off (share your Riverside
   link with the Tenable AI Accelerator Practice team).

## Outputs

Everything the skill produces is **local**: a `promo/` bundle written into your repo (value
statements, channel copy, a Riverside recording outline, visual-aid briefs, a `promo-record.yaml`,
and — only if you approve the handoff — a `handoff.yaml`), plus a pre-filled intake-form link and
on-screen coaching. It writes files and gives guidance; it submits, posts, and uploads nothing.

## Known limitations

- **Claude Code only** in v1; the Desktop / Cowork variant is a fast-follow.
- **Coaches and drafts — never a courier.** It holds no Tenable credentials, posts to no channel,
  and never acts as Tenable. The two external actions it helps with (submitting the pre-filled
  intake form, opening a listing-edit PR) run on *your* accounts, with your explicit go-ahead.
- **Video is self-serve.** It scripts the promo clip and demo and points you at a shared Riverside
  link; it does not record, edit, or host video — the team does that.
- **Truth-checks, doesn't invent.** Value statements are grounded in your listing + repo and labeled
  measured / estimate / qualitative; unverifiable claims are flagged, not asserted.

## Status

**v1** — Claude Code contributor-facing skill. The team-side ingest agent and a Claude Desktop /
Cowork variant are fast-follows (the Python helpers keep first-class Claude-native fallbacks so the
Desktop lift is clean).

## Layout

- `SKILL.md` — the runtime session spine + the three guardrail gates.
- `references/` — progressive-disclosure knowledge (voice, brand, gates, interview, capabilities, handoff).
- `assets/` — inert `promo/` bundle templates the skill fills.
- `scripts/` — five stdlib-only Python helpers (fetch listing, find PR, read vocab, scaffold, build
  intake link), each unit-tested and with a Claude-native fallback.
- `docs/intake-form-fields.md` — the intake-form field map (source of truth for the pre-fill link).
- `evals/` — behavioral gate pressure-scenarios.
- `cae-promoter.md` — the Exchange listing card (dogfooding).

## Developing

```bash
cd cae-promoter && source .venv/bin/activate && python -m pytest -q
```
