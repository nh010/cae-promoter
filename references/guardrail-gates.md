# Guardrail gates — the deep reference

SKILL.md holds the short rules; this holds the how. Three gates run on every output, plus a
hard-stop refuse list that runs before anything is produced.

## Gate 1 — Metadata-truth (generative, not just restrictive)

The gate's job is first to **generate** credible, firsthand value (see `interview.md` for the
guided five-category probe), then to **truth-check** what's claimed:

- **No invented integrations.** Anything the copy claims the asset integrates with must appear in
  the listing's `integrations[]` (from `fetch_listing`) or be confirmed in the repo. A draft that
  says "integrates with Splunk" when the listing says `["Tenable"]` is caught and refused/flagged.
- **No unsupported metric stated as fact.** A number the contributor can't ground is not asserted;
  offer to phrase it as their own attributable claim only if they confirm they measured it, else
  mark the statement `unverified`.
- **A claimed integration the repo doesn't confirm** (Hexa or any other) is not stated as fact: tell
  the contributor what you found in the repo and record it as an `unverified` review flag.
- **No fabrication.** Never invent a figure the contributor can't stand behind. The no-metric path
  (see `interview.md`) constructs a **defensible estimate** (labeled `estimate`) or degrades to
  `qualitative` — it never inflates to `measured`.
- **Hexa AI truth-check.** A contributor "yes, it uses the Hexa AI MCP" is **unproven until repo
  code/docs confirm it.** Verify against the repo before setting any `works_with_hexa` flag or
  adding a Hexa AI highlight. Assume the "yes" is wrong until the code shows the interface.

## Gate 2 — Voice / attribution

Apply the contributor-type profile from `voice-profiles.md`. The pass/fail check: does "we/us" mean
the right entity, and does the copy avoid implying the contributor is Tenable or that Tenable
authored/endorses the asset? Keep a contributor's firsthand "we cut X" (their own team); intervene
only on implied identity/endorsement.

## Gate 3 — Brand + legal

Run the `brand-rules.md` checklist over every string. Then flag (never silently strip, never
silently keep) these to `review_flags` in the promo record — **the skill flags; humans adjudicate:**

- **customer-named** — a named customer/organization in the copy.
- **third-party-cited** — a third-party research firm or its terminology (Gartner/IDC/Forrester,
  Magic Quadrant). External-facing use needs that firm's written approval — flag it.
- **competitor-ui** — a competitor's product/UI visible in a screenshot.
- **brand-rule-trip** — anything the checklist couldn't auto-fix (including a banned abbreviation
  you couldn't confidently expand to its full product name).
- **unverified** — a value statement or claimed integration the truth-check couldn't substantiate.

Keep a redacted version alongside the flag so the human has something to approve.

## Hard-stop refuse list (no output produced)

Refuse to help promote — and name the category — if the asset is any of:

- offensive / weaponized agents
- hardcoded secrets
- undisclosed outbound calls (exfiltration)
- competitor targeting
- weakening security controls

These mirror the Exchange's own reject triggers. On a hard stop, produce **no** bundle. Detect them
by scanning the **repo code**, not just the README/config — a secret or an undisclosed outbound call
usually lives in source; competitor targeting is evident from the stated purpose.

**Separately, refuse the *action* (not the asset)** when asked to **act as Tenable** — post to any
social channel as Tenable, upload to a Tenable-owned property, or push into a Tenable-owned store.
The skill holds no Tenable credentials and posts nothing; point the contributor to the local bundle
and the recording steps instead (they record at the virtual studio link Tenable emails them after
they submit the intake form). (Helping the contributor open a listing PR on *their own* GitHub auth
is allowed — see `listing-pr.md`.)
