# CAE Promoter

A Claude Code skill that helps **any** [Tenable CyberAgents Exchange](https://exchange.tenable.com)
contributor turn an already-published agent, skill, MCP server, or playbook into a polished, on-brand
promotion package — copy, video scripts, visual-aid briefs, and leaderboard optimization. Built
**community-first**: it's for community contributors above all, and works just as well for partners
and Tenable employees.

The skill name is **CAE Promoter**; the folder, slug, and invocation use the lowercase-dashed form
`cae-promoter`.

## What this does

You built something great and got it listed. Now you want people to find it, star it, and install it.
This skill turns that into a guided workflow. Run one command and it will:

1. **Interview you for real value** — a guided, five-category probe that turns "it's useful" into
   quantifiable, truth-checked value statements (measured, estimated, or qualitative — never invented).
2. **Draft your promotion bundle** — channel-ready copy for LinkedIn, X, Slack, and your listing/README,
   plus a promo-clip script, a demo outline, and visual-aid guidance, all led by your value statements
   and checked against Tenable brand rules.
3. **Pre-fill your intake form** — assembles a pre-filled link from your session so you just review
   each field and submit it yourself.
4. **Set you up to record** — after you submit the intake form, Tenable emails you a virtual recording
   studio link; the skill gets your promo-clip script and demo outline ready so you can record the
   moment it arrives.
5. **Optionally open a listing-edit PR** — on your own GitHub account, with your explicit go-ahead.

Everything it produces is **yours** — local files under `promo/` that you review, own, and post on
your own channels to drive adoption. Tenable also scouts standout contributions to amplify, so a
strong package may earn a spot on Tenable's own channels down the road (see
[Why bother?](#why-bother-drive-adoption-of-your-work) below).

## What is the CyberAgents Exchange?

The [Tenable CyberAgents Exchange](https://exchange.tenable.com) is a community directory for
cybersecurity AI agents, skills, tools, and playbooks — where security practitioners discover and
share AI-powered automation for vulnerability management, incident response, threat detection, and
more. The Exchange is an index: your source code stays in your own GitHub repo, and the listing is
metadata that points to it.

**Not listed yet?** Get listed first with the
[`cyberagents-exchange-submit`](https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder)
skill — *submit gets you listed, CAE Promoter gets you promoted.*

## What is a Claude Code skill?

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) is a markdown file that
teaches Claude Code how to run a specific workflow. Install this skill and Claude Code gains the
ability to coach you through promoting your Exchange listing: it knows the value framework, the brand
rules, the intake form, and the GitHub operations. Skills work in Claude Code and other assistants
that support the Agent Skills standard.

## Why bother? (drive adoption of your work)

- **Get discovered.** A listing with a sharp dek, real value statements, and a demo climbs the
  Exchange leaderboard (stars, Rising 🚀) and gets found.
- **Post it yourself, everywhere.** The bundle is built for *you* to share on your own LinkedIn, X,
  Slack, and README — on-brand and ready to paste.
- **Get amplified.** Tenable is actively looking for standout contributions to promote and may reach
  out about featuring your content on Tenable's own channels. A strong, truthful package is how you
  put yourself in that pool.

## Installation

### Option 1: clone to your global skills directory

```bash
git clone https://github.com/nh010/cae-promoter.git ~/.claude/skills/cae-promoter
```

The skill will be available in all projects.

### Option 2: clone to a specific project

```bash
git clone https://github.com/nh010/cae-promoter.git .claude/skills/cae-promoter
```

The skill will be available whenever you're working in that project.

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — this is a Claude Code skill (a
  Claude Desktop / Cowork variant is a fast-follow).
- **An already-published Exchange listing** for the asset you want to promote. Not listed yet? Use
  [`cyberagents-exchange-submit`](https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder)
  first.
- **Python 3.10+** for the helper scripts in `scripts/`. They're the fast path, not a hard dependency
  — each has a Claude-native fallback, so the skill still runs without Python, just more slowly.
- Optional: the **[GitHub CLI (`gh`)](https://cli.github.com/)**, authenticated as *you*, to look up
  your submission PR number and to open the optional listing-edit PR on your own account.

## Usage

1. Install the skill and run `/cae-promoter` in Claude Code.
2. Paste your **Exchange listing URL** and **GitHub repo URL** (the asset must already be published).
3. Answer the short interview — contributor type, a few profile fields, and the **guided
   value-statement probe** (pick 2–3 value categories; the skill proposes statements from your listing
   and repo for you to shape).
4. Pick the capabilities you want:

   | | Capability | What you get |
   |---|---|---|
   | **A** | Promo copy | LinkedIn, X, Slack, and listing/README drafts, led by your value statements |
   | **B** | Video | A 30–60s promo-clip script and a 2–3 min demo outline |
   | **C** | On-Exchange optimization | Leaderboard-aware listing/README copy, plus an optional listing-edit PR |
   | **D** | Visual aids | On-brand diagram, annotated-screenshot, and share-card guidance |

5. **Review the `promo/` bundle** written into your repo — you own every word and every claim.
6. **Submit the pre-filled intake form** the skill hands you: review each field, then click Submit
   (the skill never submits for you).
7. **Record when your link arrives.** Once you submit the form, Tenable emails you a virtual recording
   studio link. Record the promo clip and demo there using `promo/video/recording-outline.md`.
8. **Optionally open the listing-edit PR** on your own GitHub, then post your bundle on your channels.

## Outputs

Everything the skill produces is **local**: a `promo/` bundle written into your repo (value
statements, channel copy, a recording outline, visual-aid briefs, a `promo-record.yaml`, and — only
if you approve the handoff — a `handoff.yaml`), plus a pre-filled intake-form link and on-screen
coaching. It writes files and gives guidance; it submits, posts, and uploads nothing on your behalf.

## Good to know

- **You're in control.** The two external actions the skill helps with — submitting the pre-filled
  intake form and opening a listing-edit PR — run on *your* accounts, with your explicit go-ahead. The
  skill coaches and drafts; it never posts as you or as Tenable.
- **Recording is self-serve, on your schedule.** The skill scripts the promo clip and demo; you record
  at the virtual studio link Tenable emails you after form submission. The team edits and hosts.
- **Truth-checked, never invented.** Value statements are grounded in your listing and repo and
  labeled measured / estimate / qualitative. Unverifiable claims are flagged, not asserted.
- **Claude Code only** in v1; the Desktop / Cowork variant is a fast-follow.

## Layout

| Path | What it is |
|------|-----------|
| `SKILL.md` | The runtime session spine plus the three guardrail gates |
| `references/` | Progressive-disclosure knowledge (voice, brand, gates, interview, capabilities, handoff) |
| `assets/` | Inert `promo/` bundle templates the skill fills |
| `scripts/` | Five stdlib-only Python helpers (fetch listing, find PR, read vocab, scaffold, build intake link), each unit-tested with a Claude-native fallback |
| `docs/intake-form-fields.md` | The intake-form field map (source of truth for the pre-fill link) |
| `evals/` | Behavioral gate pressure-scenarios |
| `cae-promoter.md` | The Exchange listing card (dogfooding) |

## Status

**v1** — Claude Code contributor-facing skill. The team-side ingest agent and a Claude Desktop /
Cowork variant are fast-follows (the Python helpers keep first-class Claude-native fallbacks so the
Desktop lift is clean).

## Developing

```bash
cd cae-promoter && source .venv/bin/activate && python -m pytest -q
```
