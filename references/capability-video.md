# Capability B — video (flagship)

The **async virtual recording studio** model: one team-owned studio link produces **two
deliverables** — the floor for every contributor. The skill drafts scripts/outlines and coaches; it
never records, uploads, edits, or hosts. Fill `promo/video/recording-outline.md`.

**How the contributor gets the link:** they don't get it from the skill. After they submit the
intake form (session Step 5), **Tenable emails them their virtual recording studio link.** The
skill's job is to have their promo-clip script and demo outline ready so they can record as soon as
the link lands. No link is hardcoded here.

## Deliverable 1 — 30–60s promo clip (Claude-generated script)

The skill drafts the script from the listing + repo. It **must cover the six required elements, in
order:**

1. **Name**
2. **Job title**
3. **Organization**
4. **Asset name + type** (agent / skill / MCP server / playbook)
5. **Submission PR number** — from `find_pr` (e.g. SOC Hunter → `#59`); if unresolved, **ask the
   contributor to paste it**, never omit or invent it.
6. **Brief what + why-it-matters** — leading on the strongest verified value statement (Hexa AI /
   Tenable angle only if the truth-check confirmed it).

Frame it as a **guide, not a teleprompter** — the contributor needn't read it verbatim; it's there
to prepare from and glance back at.

## Deliverable 2 — 2–3 min demo (beat-by-beat outline)

**Five beats: intro → elevator pitch → demo → setup / config tips → CTA.** Each beat gets a rough
clock and a one-line "show this / say this" prompt, filled from the listing, the repo, and
`value-statements.md`.

1. **Intro (~0:15)** — who they are, their submission PR number, and the asset's name. (Job title
   and organization belong to the promo clip, not here.)
2. **Elevator pitch (~0:30)** — the simplest, most succinct statement of what the asset does and
   the value it delivers to them and their team. It must answer **"Why should other security teams
   deploy this agent / skill / playbook / MCP server?"**, and it **must carry at least one value
   metric** (analyst time saved, efficiency gained, false positives reduced) **or one value
   anecdote** — e.g. "surfaced 37+ net-new true positives that other automated detection missed,
   including an active insider threat, 4 MFA bypasses, and 952 critical cloud findings." Pull it
   from `promo/value-statements.md`; Gate 1 still applies, so an unverified number gets flagged,
   never invented.
3. **Demo (~1:10)** — a visual, high-level walk-through on a shared screen. Show the asset's most
   visual elements: interacting with the agent from Terminal or inside another security tool, an
   architectural map of a playbook, key charts or insights from a report the skill generated.
4. **Setup / config tips (~0:35)** — what's required to get it running, plus the best practices and
   lessons learned that get the most out of it.
5. **CTA (~0:15)** — it's on the CyberAgents Exchange; encourage people to go check it out.

**Duration: coach 2–3 minutes, and let them run over if it happens** — the clocks above plan to
~2:45 so there is slack inside the target. **The hard cap is 4:00.** When a run is heading past it,
cut beat 4 to a single sentence and point people at the README: setup detail is the least
persuasive minute in a promo demo, and it is the one beat a viewer can read instead of watch.

## Coaching + logistics

- **Screen-share checklist:** share only the demo window; hide bookmarks/notifications; hide
  customer/personal data; record at 1080p.
- **"Don't chase perfection — the team edits and finds the best moments."** The async studio gives a
  preview/re-record loop.
- **The team edits** (bumpers, sound, captions) and returns a **preview link for approval.**
- **External dependencies (team-owned, not skill work):** the emailed virtual recording studio link
  and YouTube hosting.
