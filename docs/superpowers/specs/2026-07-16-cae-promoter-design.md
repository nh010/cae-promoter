# CAE Promoter — design

> **Naming:** the skill's display name is **CAE Promoter**. Folder, slug, and slash-command
> invocation use the lowercase-dashed form `cae-promoter`.

**Date:** 2026-07-16 (rev. 2026-07-17, team-feedback rev. 2026-07-17)
**Status:** Approved (design phase), revised after the AI Accelerator Practice team demo call
(2026-07-17). Visual aids are capability D; platform facts verified via live recon. **Three
call-driven reversals/additions now baked in:**
1. **Video recording runs through Riverside**, not the contributor's own conferencing app. One
   async Riverside link funnels all recordings; async gives a preview + re-record loop (the exact
   gap that killed the earlier shared-link idea); the team edits in Riverside's backend (branded
   bumpers, sound, captions free) and returns a preview link for contributor approval. This
   replaces the conferencing-app + contributor-hosted-Drive + MP4-filename model. The **handoff
   manifest survives** but now points at the **Riverside preview/project link**.
2. **Claude Code is the v1 target; a Claude Desktop / Cowork variant is an explicit fast-follow.**
   A real population of contributors have only Claude Desktop/Cowork and would otherwise be locked
   out. The Python helper scripts stay (deterministic, cheaper on Claude Code), but every script's
   Claude-native fallback is promoted to first-class so the Desktop variant is a clean lift.
3. **Value-statement extraction is now a first-class job:** the skill probes for quantifiable
   firsthand results, feeds them into the promo bundle, helps open a **listing-page PR** (a
   **cae-promoter-owned, standalone fork→PR flow** on the contributor's own GitHub auth — *not* a
   dependency on the submitter skill), and **coaches the contributor to speak those statements
   aloud during the Riverside recording.** Also detect + highlight **Hexa AI MCP** usage (the same
   *approach* the submitter skill uses — ask, then verify against the repo — reimplemented here,
   not shared code) and any Tenable-product-pull-through angle.

The team-side **ingest agent that auto-pulls into the private team store is sub-project 2** (fast
follow), where the privileged Tenable auth legitimately lives. **YouTube hosting is a hard launch
dependency** owned by the team, not the skill (leadership is deciding public channel vs.
private-host-with-direct-links). **Deferred to post-v1:** a quotable-type value-statement tracker
sheet and integration with the customer-marketing quote process. **The v1 skill still
ships with zero Tenable credentials — it writes local files and, on approval, opens a PR from the
contributor's own GitHub account.** Next step: propagate into the implementation plan.
**Owner:** Tenable AI Accelerator Practice team

---

## Summary

cae-promoter is a **Claude Code skill**, itself listed on the CyberAgents Exchange, whose
users are *other contributors*. It coaches them to promote an **already-published**
AI asset — an agent, skill, MCP server, or playbook — both **on the Exchange** (win stars,
hit "Rising 🚀," climb the leaderboard) and **externally** (LinkedIn, X, internal Slack).

It is a **coach, drafter, and courier**: it produces Tenable-aligned, done-for-you
copy, visual aids, and do-it-yourself guidance. It writes those outputs into the
contributor's own repo. With the contributor's explicit approval, it guides the contributor to
**record their promo + demo through a shared async Riverside link** (which the team later edits
and brands), then emits a **handoff manifest** (Riverside preview/project link + metadata) that
Tenable's AI Accelerator Practice pulls from (see Courier). It may also, on approval, help the
contributor **open a PR from their own GitHub account** to add the promo section and value
statements to their listing page — via cae-promoter's own standalone fork→PR flow (no dependency
on the submitter skill).

**The credential boundary, precisely (revised on the call):** the skill holds **no Tenable
credentials** and never acts *as Tenable*. It does not post to social channels or Tenable's
YouTube, does not push into any Tenable-owned store, and does not submit anything the Practice
team must publish — those all wait for team review. The one exception is the listing PR, which
runs entirely on the **contributor's own GitHub auth** (their action, their account), exactly as
the submitter skill already does. Recording goes through the shared Riverside link the team owns;
the contributor records, the team edits and hosts. Everything else the skill emits is local files
plus the handoff manifest.

## Scope fork (context)

This design covers **sub-project 1 only**. The overall effort has two halves that share a
data contract:

- **Sub-project 1 — contributor-facing skill (this spec, build first).** Stateless; runs in
  the contributor's Claude Code context. Holds no Tenable credentials. On finish it emits a
  structured **promo record** and, with the contributor's approval, writes a **handoff
  manifest** (see Courier) — the stubbed seam to sub-project 2.
- **Sub-project 2 — team-side ingest agent + backend (deferred, its own design, fast follow).**
  Runs in the *Practice team's* context with legitimate Tenable auth (Google + Riverside). Watches
  for handoff manifests, pulls each contributor's shared bundle **and their Riverside take**,
  drives the Riverside edit (bumpers/captions), and surfaces everything for review/approve. Also
  carries the persistent datastore, legal-waiver governance, and promotable-video harvesting.
  **This is where the privileged credential legitimately lives** — never in the contributor-side
  skill.

The seam between them is the **promo record** (see Data contract).

**Platform reach (decided on the call): Claude Code v1, Claude Desktop / Cowork variant is a
fast-follow.** A real population of contributors have only Claude Desktop or Cowork (no Claude
Code) and would otherwise be locked out — submitter-skill users hit this today. v1
targets Claude Code (where the Python helpers run deterministically and cheaply), but **every
helper script keeps a first-class Claude-native fallback** so a Desktop variant is a clean lift,
and the Claude Code SKILL.md carries a short **routing note** ("on Claude Desktop, use the Desktop
variant"). The Desktop variant itself is deferred alongside sub-project 2 — same fast-follow
horizon.

## Users

Three contributor types. The skill adapts voice and guardrails per type:

| Type | Voice / attribution rule |
|------|--------------------------|
| **Tenable employee** | May speak *as* Tenable, within brand/editorial rules. "We/us" = Tenable. |
| **Tenable partner** | **"We/us" = the partner's own company/team** (encouraged — it's their result). May state the Tenable relationship, but must not speak *as* Tenable or imply Tenable authored or endorses the asset. Co-marketing caution. A genuine third profile, not "employee lite." |
| **External community** | **"We/us" = the contributor's own organization/team** (encouraged). Speaks in their own voice. May reference Tenable / the Exchange factually, but never speak *as* Tenable or imply endorsement. |

> **On "we/us" (clarified):** partner and community contributors are *encouraged* to use "we/us" for
> their **own** organization or team — the value statements are their firsthand results ("we cut MTTR
> by 88%"). The only line is that they must not phrase it as if they were **Tenable** ("we at Tenable
> …," "our platform" meaning Tenable's). In practice this is a low-risk edge case that matters mainly
> for **what gets posted on the Exchange**; the voice/attribution gate checks it there, not in every
> internal draft.

## Architecture

A Claude Code **skill** is the front door. It runs inline in the contributor's session,
converses turn by turn (needed to elicit firsthand metrics), and writes files into the
contributor's workspace. Under the hood it **may** dispatch subagents for heavy,
context-heavy work (e.g., deep-reading a large repo and returning a structured summary) to
keep the main context clean. The thing we ship and list on the Exchange is a skill.

Rationale for skill over agent: on the Exchange, "skill" / "agent" / "mcp-server" /
"playbook" are *listing categories*, not build choices. A skill listing carries
`compatible_platforms: ["Claude Code"]` and an `invocation` slash command — exactly
cae-promoter's shape. An isolated subagent would fight the interactive claim-elicitation
loop. The official `cyberagents-exchange-submit` skill (the Submission Builder) is a working
near-twin one step earlier in the funnel: submit gets you *listed*, cae-promoter gets you
*promoted*. It's a **reference and a sibling, not a dependency** — cae-promoter reimplements the
pieces it needs (the fork→PR flow, the Hexa verify approach) standalone rather than importing or
calling the submitter skill, so the two ship and version independently.

## Session flow (guided menu)

0. **Preflight — a published listing is required.** cae-promoter promotes an asset that is
   **already published on the Exchange**; it is not a pre-publish tool. The skill first confirms a
   real listing exists at the given URL and that it is **not** a seeded example
   (`visibility: example`, like `aristaeus-threat-to-board`). If there's no listing yet — or only a
   seed — the skill **stops and points the contributor to the `cyberagents-exchange-submit` skill
   first** ("get listed, then get promoted"). This precondition is also what guarantees a real
   submission PR exists for the promo clip (see step 1 and Capability B).
1. **Ingest.** Contributor pastes **both** their Exchange listing URL **and** their GitHub
   repo URL. The skill:
   - Reads the **listing** for positioning, controlled-vocab integrations, and tags.
   - Deep-reads the **repo** (README, config, key source files) for substance and to verify
     claims.
   - Loads **platform knowledge** from `tenable/cyberagents-exchange` (CONTRIBUTING.md,
     templates, validator vocab, contributing checklist) so Exchange advice is real.
   - **Looks up the contributor's submission PR number** in `tenable/cyberagents-exchange` from
     the slug (needed for the promo clip; see Capability B). Because preflight guarantees a
     published listing, a real PR exists; the lookup only falls back to asking if the search is
     ambiguous or the PR title/branch never named the slug.
2. **Interview / identify.** A short up-front interview does three things (agreed on the
   call): (a) ask contributor type (employee / partner / community) → select voice + guardrail
   profile, and assemble the **contributor profile the intake form needs** on a strict
   **derive-first, ask-only-the-gaps** basis — the skill first fills every field it can from what it
   already knows (the ingest of the Exchange listing page and GitHub repo, plus the session), then
   asks the contributor **only** for what it genuinely can't determine and to confirm anything
   inferred. Concretely: **name, GitHub handle, organization, and often job title** are usually
   derivable from the listing `author`/`github_url` and the repo profile/README, so the skill
   proposes them for a one-tap confirm rather than asking cold; **work email, region, industry,
   organization size, and security-team size** typically aren't discoverable and are asked (region
   and industry mapped to the form's fixed option list; the two sizes ask for a specific number
   first, falling back to a fixed range only if the contributor declines); **future-outreach
   consent** [yes/no] is always asked (it's a permission, never inferred). The bar: minimize
   questions — never ask for something the skill could have derived, and batch the true unknowns
   into as few prompts as possible; (b) **run the guided value-statement probe** — present five value categories, have the
   contributor pick the 2–3 that best fit (or "Other"), propose three statements grounded in the
   listing + repo, and let them adjust/revise; when there's no measured number, help construct a
   defensible estimate, labeling it an estimate (degrade to qualitative only if even that's
   impossible). See **The value-statement probe** section above for the full flow and the
   metadata-truth gate for truth-status; (c) **detect Hexa AI MCP usage** — ask, then verify against the repo code/docs
   (mirroring the submitter skill, which assumes a "yes" is unverified until the code confirms
   it), and surface any Tenable-product-pull-through angle to highlight within brand rules.
3. **Menu.** Contributor picks one or more of the four capabilities below.
4. **Emit.** Write outputs as files into a `promo/` folder in the contributor's repo, and
   produce a **promo record**. Extracted value statements flow into the copy (A), the demo/promo
   talking points (B), and the listing PR (C).
5. **Intake form (pre-filled link, contributor submits).** Once the value statements are confirmed
   (step 2b) and the bundle is emitted — and **before** the recording — the skill builds a
   **pre-filled Google Form link** for the CyberAgents Exchange Contributor Promotion Intake Form
   from the profile + value statements already gathered, and hands it to the contributor to
   **review and submit themselves**. The skill never POSTs on their behalf: the pre-fill just
   saves typing; the contributor sees every answer and clicks Submit. This is the single moment the
   intake data reaches the team, and placing it after value-statement confirmation means every field
   is settled before the link is built. See **Intake form** below.
6. **Approve & hand off (courier).** Show the contributor exactly what the bundle contains,
   capture an explicit approval, then: (a) guide them to **record through the shared async
   Riverside link**; (b) write the handoff manifest with the Riverside preview/project link (see
   Courier); (c) optionally help them **open a listing-page PR from their own GitHub account**.
   Approval is per-session and logged in the promo record; declining leaves everything local, no
   manifest written and no PR opened.

## The value-statement probe (guided, five categories)

The heart of the interview (step 2b) is a **guided, category-driven probe**, not an open-ended
"got any metrics?" question. It runs in four moves:

1. **Present five value categories and ask the contributor to pick the 2–3 that best reflect their
   tool's value** (plus an **"Other — please specify"** for value the list misses):
   1. **Operational efficiency** — e.g. "We reduced investigation time from 45 minutes to 8 minutes."
   2. **Risk reduction** — e.g. "We reduced exploitable critical exposures by 72%."
   3. **Faster response** — e.g. "We reduced our mean-time-to-respond (MTTR) by 88%."
   4. **Better decisions** — e.g. "False positives dropped 65% while detection coverage increased."
   5. **Scale without headcount** — e.g. "Our existing team now manages 3x more assets without
      additional analysts."
2. **Propose three value statements** aligned to the selected categories, drafted from the skill's
   **analysis of the Exchange listing + the GitHub repo** (what the tool actually does), so the
   proposals are grounded in the real asset rather than generic.
3. **Contributor reviews and shapes them.** They adjust the actual numbers/estimates, request
   revisions, or replace a statement with an entirely different one. This is the step where each
   statement's truth-status is set — **measured / estimate / qualitative** (see the metadata-truth
   gate and its no-metric path): the contributor confirms a real figure, grounds an estimate, or
   accepts a qualitative framing.
4. **Vary the framing.** The skill deliberately varies sentence structure across statements so that
   what lands on the Exchange doesn't read as boilerplate — statements needn't be unique, but some
   variety and creativity is encouraged (e.g. lead with the number in one, the outcome in another,
   the before/after in a third).

The 2–3 shaped statements are written to `promo/value-statements.md` (each with its category and
truth-status) and become the spine of the copy (A), the recording talking points (B), and the
listing PR (C). Voice/attribution still applies — the "we/our" phrasing in the category examples is
tuned per contributor type (employee / partner / community).

## Capabilities (v1)

### A. Written promo copy
Channel-specific drafts: LinkedIn, X/Twitter, an internal Slack blurb, and a listing/README
promo section. Voice per contributor type. Every draft leads with the **quantifiable value
statements elicited in the interview**, not a feature list, and highlights **Hexa AI MCP** and
any Tenable-product-pull-through angle where the truth-check confirms it.

> **Riverside also auto-suggests social / blog / newsletter copy** from a recording. When
> a contributor records (capability B), the team can lift and tweak that suggested copy rather than
> only relying on the skill's drafts. The skill's copy is the pre-recording draft; Riverside's is a
> post-recording complement — not a competing source of truth. Where they overlap, the skill's
> brand-checked copy governs the written bundle.

### B. Video production guidance (flagship) — Riverside async
Recording runs through **one shared async Riverside link** the Practice team owns (reversed from
the earlier conferencing-app plan on the 2026-07-17 call). **The link is not stored in this skill.**
There is a single team-owned invitation every contributor records through, and the Practice team
distributes it directly by email; the skill never carries or mints one. The skill's job is the
**pre-work and the coaching**, not hosting: it tells the contributor exactly what to cover, then
points them at the link the team sent them. Riverside gives a **preview + re-record loop** at
the end of an async capture (the missing
piece that killed the earlier one-shot shared-link idea), so contributors can watch their take and
redo it until they're happy.

**Two deliverables from one Riverside session (the floor for every contributor):** a **30–60s promo
clip** and a **2–3 min demo**. One session avoids the two-link drop-off; two structured deliverables
give the team the raw material it actually needs. Both are scaffolded so a non-presenter never faces
an open mic — the promo clip is *scripted* by the skill; the demo is a beat-by-beat outline.

- **30–60s promo clip — Claude-generated script (a guide, not a teleprompter).** From the
  contributor's listing and repo, the skill drafts a tight 30–60s script for their review. It must
  cover, in order, **six required elements** (this is the structure the team standardizes on):
  1. **Name** — the contributor's full name.
  2. **Job title.**
  3. **Organization name.**
  4. **Asset name + type** — the agent / skill / MCP server / playbook, by its listing name.
  5. **Pull request number** — the contributor's PR to `tenable/cyberagents-exchange` (e.g. SOC
     Hunter is `#59`); the skill looks this up automatically (see below), falling back to asking.
  6. **A brief what + why-it-matters** — what they built and why it matters, in the remaining seconds.
  The contributor **need not read it verbatim** — it's a reference to prepare from and glance back
  at while recording. The script leads on the strongest verified value statement where one exists,
  and folds in the Hexa AI / Tenable-pull-through angle if the truth-check confirmed it.
- **2–3 min demo — beat-by-beat outline.** A deliberate, tight live demo (problem → what it does →
  install/config → value → where to get it), each beat with a rough clock and a one-line "show this
  / say this" prompt, plus the screen-share checklist. Structured, not free-form.

Coaching mantra from the call sits at the top of both: **don't chase perfection — the team edits and
finds the best moments; just get a clean take.** The scaffolds are guides, not straitjackets.

**Finding the PR number.** The skill resolves the contributor's submission PR against
`tenable/cyberagents-exchange` automatically — verified path (2026-07-17): the GitHub search API
`GET /search/issues?q=repo:tenable/cyberagents-exchange+type:pr+<slug>` returns the listing PR in one
call (SOC Hunter `soc-hunter` → `#59`; confirmed across several real listings, e.g. `#39`, `#15`,
`#28`). It prefers the `gh` CLI (authenticated, higher rate limit) and falls back to unauthenticated
`curl`. Because the preflight step already required a **published, non-example listing**, a real
submission PR exists — seeded examples like `aristaeus-threat-to-board` (which have no PR) are turned
away before this point. The lookup only **asks the contributor to paste their PR number** in the
narrow case where the search is ambiguous or the PR's title/branch never named the slug.

The skill supplies: the **promo-clip script** + the **demo outline** (each with a rough clock and
"say this here" prompts), a short **screen-share checklist** for the demo (share only the demo
window, hide bookmarks/notifications, 1080p), and the framing that **the team does all editing in
Riverside** — branded bumpers, sound, captions (free), quick cuts — then returns a **preview link for
the contributor's final review and approval.** That edit/approval step is manual by design and
outside the contributor's critical path.

**Video handoff.** There is no contributor-hosted MP4 and no filename convention. The contributor
records into the shared Riverside link; the skill records the **Riverside preview/project link** in
the handoff manifest so the Practice team can pull the take, edit, and (per the YouTube launch
dependency) host it. The skill uploads nothing and holds no Tenable credentials.

> **External dependencies (team-owned, not skill scope):** (1) the **shared Riverside link** and,
> eventually, the **Riverside MCP server** (waitlist — the team is on it) that could automate parts of
> this; (2) **YouTube hosting** — leadership is deciding between a public channel and a
> private-host-with-direct-links option for launch, but *some* YouTube home is required at launch.
> Until the Riverside MCP lands, the link hand-off is manual; until YouTube hosting is decided, the
> on-listing video advice is "link the demo from your README" (see capability C).

### C. On-Exchange optimization (+ listing PR)
Using platform-repo knowledge, concrete edits to the listing and README to earn
stars/installs: a sharper dek, correct integrations/tags from the controlled vocabulary, a
stronger "What it does," the **quantifiable value statements** woven in, the **`works_with_hexa`
flag/badge** where the truth-check confirms it, and README quality checked against Exchange norms
and requirements. Success is framed against real signals (stars, installs, Rising 🚀).

**Opening the listing PR (new on the call).** On explicit approval, the skill helps the
contributor **open a PR against `tenable/cyberagents-exchange` from their own GitHub account** to
apply these edits, using **cae-promoter's own standalone fork→PR flow** — the submitter skill does
the same thing, but we reimplement it here rather than depend on its code, so the two skills ship
and version independently. This is the one action the skill assists that writes to a **public**
surface, and it runs entirely on the **contributor's own auth** (their action, their account); it
uses **no Tenable credentials** and never acts as Tenable. Declining leaves the edits as local
suggestions in the bundle only. (The intake form is the other contributor-driven external action,
but it's a **private** submission to the Practice team via a pre-filled link the contributor
submits themselves — see Intake form; likewise no Tenable credential and the contributor's own
click.)

The fork→PR flow is a straightforward sequence on the contributor's own `gh`/git auth: confirm
`gh auth status`, fork `tenable/cyberagents-exchange` (or reuse an existing fork), branch, edit the
listing file (`<type>/<slug>.md`) plus any README changes, commit, push, and open the PR with a
generated title/body. On Claude Code it runs via `gh`/git commands; the Claude-native fallback (for
the deferred Desktop variant) walks the contributor through the same steps by hand — the workaround
submitter-skill users who lack Claude Code already rely on.

> **Video-on-listing is an external platform dependency, not skill scope.** Approved demo
> videos are meant to appear as embedded YouTube on the listing page (from the Practice
> team's channel). The listing schema has **no video field today** (verified: `validator.py`
> `Entry` has no `video`/`youtube`/`embed`), and the website has no embed component — the one
> existing listing with a demo video just links to it from its README. Adding a `video_url`
> field to `validator.py` and an embed component to the website is **Exchange-platform work in
> two repos cae-promoter does not own** (the public content repo plus the private website repo),
> tracked as a dependency the team sequences separately. Until it lands, the skill's on-Exchange
> advice for video is "link the demo from
> your README" (the current norm). Once the field exists, drafting the `video_url` listing
> edit can fold into this capability.

### D. Visual aids
Tenable-brand-aligned visual assets the contributor can drop into a listing, README, or
social post. Built on the workspace brand system (hexagon grid, one-color icons, approved
color combos, Work Sans, no photography for products/concepts):

- **Diagram guidance / specs** — a hexagon-grid "how it works" or before/after diagram
  describing the asset's flow, delivered as a spec the contributor (or the team) can render.
- **Screenshot annotation guidance** — which screens to capture and how to annotate them
  on-brand (callouts, blurring customer data, no competitor UI).
- **Social/OG card copy + layout** — text and layout direction for a share card, within
  brand rules (sentence case, single yellow highlight, no yellow-on-white).

Visual aids obey the same three guardrail gates. Anything requiring a real design tool or
human rendering is delivered as clear, on-brand direction rather than a finished raster.

### Cut from v1
- **E. Promotion strategy/plan** — deferred. May return in a later version.

## Guardrails — three gates on every output

1. **Metadata-truth (generative).** Because contributors have run their own asset in their
   own environment, the skill **proactively probes** for firsthand, quantifiable **value
   statements** (time saved, alerts triaged, hours per week, false positives reduced, risk
   reduced) in the interview and helps phrase them as credible, attributable claims. These
   statements are the spine of the copy, the recording talking points, and the listing PR.
   **No-metric path (decided):** when a contributor has no measured number, the skill **helps them
   construct a defensible estimate** from what they *do* know (e.g. "it replaced a manual task you
   ran ~daily that took ~2 hours → roughly 10 hours/week"), recording the reasoning and labeling the
   result an **estimate** (not a measured figure). Only if even a grounded estimate is impossible
   does it fall back to **qualitative** value ("cut a tedious step," "fewer false alarms"), flagged
   as unquantified. It never blocks the bundle for lack of a hard number, and never inflates one.
   Truth-checking still applies: **no invented integrations** (checked against the listing's
   `integrations[]`), **no unsupported metrics** (an estimate is labeled as such, an invented one is
   refused), and the **`works_with_hexa` claim is verified against the repo code/docs** before any
   Hexa AI badge or highlight — a contributor's unverified "yes" is treated as unproven until the
   code confirms it (mirroring the submitter skill). Anything that can't be substantiated is
   labeled (estimate / unverified / qualitative) rather than dropped or asserted as fact.
2. **Voice / attribution (per contributor type).** Enforces the employee / partner /
   community rules in the Users table.
3. **Brand + legal.** Applies the workspace Tenable brand/editorial rules (product naming,
   casing, em-dash discipline, contractions). Flags anything needing review — customer
   names, third-party citations, competitor UI in screenshots — into the promo record. The
   skill **flags; humans and the backend adjudicate.** (Analyst-firm citation restriction is
   removed for now.)

The skill must also refuse to help promote anything the Exchange rejects outright:
offensive/weaponized agents, hardcoded secrets, undisclosed outbound calls, competitor
targeting, or weakening of security controls.

## Intake form (pre-filled link)

The **CyberAgents Exchange Contributor Promotion Intake Form** is the one channel by which the
contributor's identity, profile, and value statements reach the Practice team as structured data.
The skill does **not** submit it — it builds a **pre-filled link** the contributor reviews and
submits, preserving the same "nothing leaves the machine without the contributor's own action"
guarantee that governs the listing PR.

- **Placement:** after the value statements are confirmed (step 2b) and the bundle is emitted,
  **before** the recording (step 5 in the session flow). The confirmed value statements and profile
  are exactly what the form needs, so building it here means every field is settled; capturing it
  before recording also means the contributor's details and value claims are on record before they
  step in front of the camera.
- **Mechanism:** the skill appends URL-encoded `entry.<id>=<value>` pairs to the form's viewform
  URL, opens/prints the link, and tells the contributor to **review every field and click Submit**.
  No unauthenticated POST, no Tenable credential, no Forms API dependency at runtime. The form must
  stay openly responder-accessible (no forced sign-in, no one-response limit) for pre-fill to work.
- **Field sources (derive-first):** the skill fills every field it can **before** asking. Asset
  identity (asset name, build type, listing URL, repo URL) comes from preflight + ingest; **name,
  GitHub handle, organization, and often job title** are derived from the listing
  `author`/`github_url` and the repo profile/README and offered for a one-tap confirm; the three
  value statements come from `promo/value-statements.md`. Only the genuinely non-derivable fields
  are asked in the interview — **work email, region, industry, organization size, security-team
  size** — plus **future-outreach consent**, which is always asked because it's a permission, not a
  fact. See step 2 for the full derive-vs-ask split.
- **Choice fields must match a listed option or use "Other."** Region, industry, contributor type,
  and build type are required multiple-choice; pre-fill selects a **listed** option only on an exact
  string match. **Region and industry each have a real "Other" free-text option**, so an answer that
  isn't on the list still pre-fills cleanly via Google's two-param "Other" mechanism
  (`entry.<id>=__other_option__` + `entry.<id>.other_option_response=<text>`) — the skill prefers a
  listed option on an exact match, else sends "Other" + the contributor's own words. Contributor
  type and build type have **no** "Other" (both are always known from the interview/ingest, so they
  map exactly). See `docs/intake-form-fields.md` for the "Other" param details.
- **Size fields are specific-first.** Organization size and security-team size are open text: the
  skill inserts the contributor's specific number when given, and only falls back to one fixed range
  string (from the range ladder) if they decline — so the column stays consistent and a range reads
  as visibly distinct from a real count.
- **Consent:** the pre-fill link *is* the consent moment for the intake data — the contributor sees
  every value before submitting. Declining to submit is allowed and leaves the promo record noting
  the form was offered but not submitted; it does not block the rest of the session.

The exact field-to-`entry.<id>` map, option strings, and range ladders live in
`docs/intake-form-fields.md` (extracted live from the form; the source of truth for the builder).

## Courier — approved handoff to the team

**The review boundary is the AI Accelerator Practice, not Tenable-vs-outside.** A Tenable
employee who contributes an asset is *outside* the review process exactly like a partner or
community member — most Tenable employees are not on the Practice team that reviews and
approves CAE promotional content. So **all three contributor types use one uniform handoff**;
there is no employee fast-lane.

**Design constraint (physics, not policy):** writing into a private, team-owned destination
requires team-owned auth. The skill runs in the *contributor's* context and holds **no Tenable
credentials** — so the skill can never push into the team's private store, and we will not bake
a Tenable credential into software distributed to contributors. The privileged write therefore
lives entirely on the team side (sub-project 2).

**Model (revised on the call): text stays local, video goes through Riverside, manifest points at
both.** Two things ride separately now:
- **The written bundle** (copy, talking-point outlines, visual-aid specs, promo record) stays in
  the contributor's own repo `promo/` folder, exactly as before.
- **The video** is recorded through the **shared async Riverside link the team owns** — not a
  contributor Drive. The contributor records; the team edits/brands/hosts. This removes the earlier
  contributor-hosted-Drive step entirely.

The skill emits a small **handoff manifest** that points the Practice team (sub-project 2, fast
follow) at the **Riverside preview/project link** to pull the take, plus the identity/flags it
needs to route. If the contributor also opened a **listing PR** (capability C, their own GitHub
auth), the manifest records the PR URL so the team can track it. One team-controlled recording
destination (Riverside); zero Tenable credentials in the skill.

### What the v1 skill does (this spec)

On the contributor's explicit approval, the skill:

1. **Packages the bundle locally** into the `promo/` folder in the contributor's repo:

   ```
   promo/
     promo-record.yaml       # the data contract (see below)
     value-statements.md     # the extracted, truth-checked quantifiable claims
     copy/         linkedin.md · x.md · slack.md · listing-section.md
     video/        recording-outline.md   # two-part talking points + demo beats (no MP4)
     visual-aids/  diagram-spec.md · screenshot-guide.md · card.md
     README.md               # human-readable index of this drop
   ```

2. **Guides the contributor to record** through the **shared async Riverside link** (team-owned)
   using the two-part `recording-outline.md`, and to paste back the **Riverside preview/project
   link**. The skill never records, uploads, or holds any Tenable credential.
3. **Optionally helps open the listing PR** (capability C) from the contributor's own GitHub
   account, and captures the resulting **PR URL**.
4. **Writes the handoff manifest** (`promo/handoff.yaml`): Riverside link, contributor type, asset
   identity, which capabilities ran, video-planned flag, listing-PR URL (if any), and the review
   flags. This manifest is the **stubbed seam** to sub-project 2.

### Stub vs. fast follow

- **v1 (stub, this spec):** the manifest is written **locally** and the skill prints exact
  next steps ("share this Riverside link with the Practice team"). No automated transmission; a
  human relays the link once. This keeps the contributor-side skill free of any privileged
  credential and shippable on its own.
- **Sub-project 2 (fast follow):** the team-side ingest agent watches for manifests, pulls each
  contributor's Riverside take (and reads the bundle from the linked repo), drives the Riverside
  edit, and surfaces it for review — eliminating the last manual touchpoint. The **manifest schema
  is the contract** the ingest agent reads; where the manifest lands so the agent sees it without a
  human relay is the first design decision for sub-project 2. The **Riverside MCP server**
  (waitlist) may automate the pull once available.

### Consent and guarantees

- **Consent gate:** the handoff is prepared **only** after the contributor sees exactly what
  the bundle contains and explicitly approves. Declining leaves everything local; no manifest
  is written and no PR is opened. Approval is per-session, logged in the promo record.
- **What it never does:** it does not post to social channels or Tenable's YouTube, does not push
  into any Tenable-owned store, and holds no Tenable credentials. The two contributor-driven
  external actions it assists both run on the contributor's own action and never on a Tenable
  credential: the **listing PR** (public, on the contributor's own GitHub auth, on approval) and the
  **intake form** (a private submission to the Practice team via a pre-filled link the contributor
  reviews and submits). Everything else it emits is local files + the handoff manifest + coaching.
- **Sensitive content:** the consent screen calls out anything flagged sensitive (customer name,
  unreleased detail, competitor UI) so the contributor decides what to include **before recording,
  before the PR, and before sharing the Riverside link.**

**Team input needed for the fast follow (not for v1 ship):** where the manifest lands so the
ingest agent can pick it up, standing up that team-side agent with legitimate Tenable auth
(Google + Riverside), and the YouTube hosting decision. The v1 skill ships without any of this.

## Data contract — the promo record and the handoff manifest

Two artifacts, both written into `promo/` at the end of a session:

**`promo-record.yaml` — the session record** (describes what was produced):

- Asset identity: Exchange listing URL, GitHub repo URL, listing type, slug, and the
  **original listing PR number** (the contributor's submission PR, e.g. `#59`; looked up, or
  pasted by the contributor if the lookup found nothing). This is the number spoken in the promo
  clip — distinct from any *new* promotion-edit PR below.
- Contributor type (employee / partner / community).
- **Contributor profile** gathered for the intake form (name, job title, organization, work email,
  GitHub handle, region, industry, organization size, security-team size, future-outreach consent),
  with each field marked **derived vs. asked** so the record shows what was inferred vs. confirmed.
- **Intake form:** whether the pre-filled link was built and whether the contributor reported
  submitting it (offered / submitted / declined). The skill can't confirm a submission server-side,
  so this is the contributor's own report; declining does not block the session.
- Assets generated this session (which capabilities ran; file paths under `promo/`).
- **Value statements** extracted (and which are truth-checked vs. flagged unverified).
- **Hexa AI:** `works_with_hexa` claim + whether the repo verified it.
- Video planned? (boolean; recorded via Riverside — a 30–60s promo clip + a 2–3 min demo).
- **Promotion-edit PR:** opened? (boolean + PR URL if so — the *new* capability-C PR, not the
  original listing PR).
- Flags for human review (waiver needed, customer named, third-party cited, brand-rule trip).
- **Approval:** whether the contributor approved the handoff (boolean); if declined, no
  manifest is written and no PR is opened.
- Timestamp (stamped by the host, not generated inside a workflow).

**`handoff.yaml` — the manifest / seam to sub-project 2** (tells the team-side ingest agent
where to pull from). Written only on approval:

- The **Riverside preview/project link** to the contributor's take (when a video was recorded).
- The **listing-PR URL** (when the contributor opened one).
- A copy of the identity + flag fields the ingest agent needs to route and prioritize.
- Manifest schema version (so the ingest agent can evolve independently).

## Outputs

The written bundle is all written to a `promo/` folder in the contributor's own repo (their
storage, their control). The **video** is recorded through the team-owned shared Riverside link;
the manifest points the team-side ingest agent (sub-project 2) at the Riverside preview/project
link (and the listing-PR URL, if one was opened) for a clean, pull-based harvest.

## Verified platform facts (live recon, 2026-07-17)

Confirmed against the live site and repos so the plan rests on facts, not assumptions:

- **Production host:** `exchange.tenable.com`. The site is an **index, not a code registry** —
  each listing is metadata pointing to the author's own GitHub repo.
- **Machine-readable listing endpoints — only two of four actually serve JSON (verified
  2026-07-17, re-checked at plan time):** `/api/agents.json` and `/api/playbooks.json` return
  real JSON arrays. **`/api/skills.json` and `/api/mcp-servers.json` fall through to the SPA's
  `index.html`** (identical 29,877-byte HTML bodies) despite a misleading
  `content-type: application/json` header — they are NOT usable. The platform's own `/llms.txt`
  and `/llms-full.txt` document *only* the agents and playbooks endpoints, confirming this is by
  design, not a transient outage. The live JSON also omits the `type`/`framework` fields that
  `llms-full.txt` describes. **Resolution: the skill's canonical ingest source is the public
  content repo `tenable/cyberagents-exchange`, which serves every listing uniformly as
  `<type>/<slug>.md` frontmatter** (raw:
  `raw.githubusercontent.com/tenable/cyberagents-exchange/main/<type>/<slug>.md`; verified for
  `agents/` and `skills/`). This is the same source of truth that feeds both the JSON endpoints
  and `validator.py`, so it never disagrees with the schema. Per-listing frontmatter fields:
  `name`, `author`, `github_url`, `description`, `license`, `tier` (`contributed` /
  `community-reviewed` / `certified`), `tags[]`, `integrations[]`, `date_added`, plus
  type-specific fields (`compatible_platforms` + `invocation` for skills, `compatible_clients` /
  `transport` / `auth_method` / `runtime` for MCP servers, `playbook_type` / `agents_used` for
  playbooks). The agents/playbooks JSON endpoints remain a fast path when the listing type is
  agent or playbook. → **Ingest reads the content repo (or the two working JSON endpoints); no
  HTML scraping.**
- **Two-repo architecture:** the website source is a private Tenable-owned repo;
  **content/listings are public in `tenable/cyberagents-exchange`.** The site builds from the
  public content repo, so the content repo is the reliable read target either way.
- **Controlled vocab lives in `validator.py`** (pydantic `Entry` model, `Literal[...]` enums
  for `integrations`, `tier`, etc.) — raw-fetchable at
  `raw.githubusercontent.com/tenable/cyberagents-exchange/main/validator.py`. → **Read live;
  never hard-code the vocab.** `CONTRIBUTING.md`, `templates/`, and per-type dirs confirmed present.
- **Leaderboard / success signal (`src/lib/leaderboard.ts`) — the thing to optimize toward:**
  - **Primary rank = raw GitHub `stars`**, tie-broken by `rising`, then most-recent `pushedAt`.
  - **Rising 🚀 = top 20% by stars-per-day among listings ≤ 90 days old.** New contributors
    can earn Rising through early star *velocity* long before absolute star counts matter —
    the single most actionable coaching lever for a fresh listing.
  - Stats harvested per repo: `stars`, `forks`, `watchers`, `pushedAt`. Keeping the repo
    actively pushed is a real recency tiebreaker.
- **Listing/promotion mechanism = PR to `tenable/cyberagents-exchange`** (fork → add listing
  → PR). cae-promoter reimplements this fork→PR flow standalone (not a dependency on the submitter
  skill) for the promotion-edit PR.
- **Submission-PR lookup (verified 2026-07-17):** `GET /search/issues?q=repo:tenable/cyberagents-exchange+type:pr+<slug>`
  returns the contributor's listing PR in one call — `soc-hunter` → `#59`, `cloud-risk-triage-suite`
  → `#39`, `tenable-host-doctor` → `#15`, `company-intel-studio` → `#28`. Prefer `gh` (auth, 30
  req/min search limit) over unauthenticated `curl` (10/min). PR titles follow "Add listing: <Name>",
  branches `add-<slug>`.
- **Preflight signal — seeded examples carry `visibility: "example"`** (verified: `validator.py`
  `Entry.visibility: Literal["example"] | None`; `aristaeus-threat-to-board` has it set and has **no
  contributor PR**). The skill treats a missing listing *or* a `visibility: example` listing as "not
  eligible yet → go use `cyberagents-exchange-submit` first." Every real, non-example published
  listing has a discoverable submission PR.

## Grounding sources

- **The contributor's asset:** their Exchange listing + their GitHub repo.
- **The platform:** `tenable/cyberagents-exchange` — CONTRIBUTING.md, `templates/*`,
  `validator.py` (controlled vocab), `docs/contributing_checklist.md`, Contribution Agreement.

## Open risks (resolve at build time, not now)

- **GitHub access (read + contributor-auth write):** public community repos are fine for reads;
  private Tenable repos would need an auth story. Rate limits on repo fetching and on the PR-lookup
  search API (10/min unauth, 30/min via `gh`). The **promotion-edit PR (capability C) writes to
  GitHub on the contributor's own auth** via cae-promoter's own standalone fork→PR flow — no Tenable
  credential involved; the risk is the usual contributor-auth/fork edge cases, not a baked-in
  privileged token.
- **Preflight (published-listing requirement):** the skill is for already-published assets only. It
  turns away contributors with no listing or a `visibility: example` seed, pointing them to
  `cyberagents-exchange-submit` first. Edge case to handle at build time: a listing that exists but
  whose submission PR can't be auto-resolved → ask the contributor to paste the PR number.
- **Riverside dependency (v1):** the shared async link must exist and be team-owned before the
  video capability is usable; the Riverside MCP server (waitlist) is a later automation, not a v1
  requirement. The link hand-off is a manual relay in v1.
- **YouTube hosting (launch dependency, team-owned):** a public channel vs. private-host-with-
  direct-links is a leadership decision; the skill's on-listing video advice stays "link the demo
  from your README" until it's resolved.
- **Manifest seam (sub-project 2, not v1):** where the handoff manifest lands so the ingest
  agent picks it up without a human relay is a sub-project 2 design decision; v1 ships with the
  manifest as a local file + one-time human relay. See Courier.
- **Listing JSON endpoint (RESOLVED 2026-07-17):** only `/api/agents.json` and
  `/api/playbooks.json` serve JSON; skills/mcp-servers 404 into SPA HTML. The skill ingests
  listing frontmatter from the content repo (`<type>/<slug>.md`) as the uniform, reliable path,
  using the two working JSON endpoints only as an agent/playbook fast path. See verified facts.
- **Controlled vocabulary drift:** `validator.py` is the source of truth and changes; the
  skill should read it live rather than hard-code values.

## Non-goals (v1)

- **Pre-publish promotion.** The skill promotes an already-published listing; it does not help draft
  or submit the listing itself (that's `cyberagents-exchange-submit`). No listing → the skill stops
  and refers the contributor there.
- Auto-posting to **social channels or Tenable's YouTube**, or acting as Tenable anywhere. The
  skill assists two contributor-driven external actions, both on the contributor's own action and
  neither on a Tenable credential — the **promotion-edit PR** (public, contributor's GitHub auth, on
  approval) and the **intake-form submission** (private, via a pre-filled link the contributor
  submits) — and otherwise only writes local files + the handoff manifest. It never **auto-submits**
  the form; the pre-fill only saves typing.
- Recording, editing, or hosting video itself — that runs through the team-owned Riverside link and
  the team's edit/host process. The skill supplies the outline and records the link.
- The team backend (sub-project 2) — the courier delivers *to* its intake; the datastore,
  waiver governance, and video harvesting are still deferred.
- The **Claude Desktop / Cowork variant** — v1 targets Claude Code; the Desktop variant is a
  fast-follow (scripts keep first-class Claude-native fallbacks to make it a clean lift).
- A **quotable-type value-statement tracker sheet** and integration with the customer-marketing
  quote process — deferred to post-v1 (ship v1, then review with customer marketing).
- Promotion strategy/plan capability (E).
- Analyst-firm citation gating.
- Multi-language output.
