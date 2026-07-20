# CAE Promoter evals — how to run

These are **behavioral evals**, not CI. They test whether the skill's guardrail gates hold under
pressure — something unit tests can't cover. Run them manually (or via a subagent) in a fresh
session.

## How to run

1. Start a **fresh Claude Code session** with the `cae-promoter` skill active (installed/loaded).
2. Open `gate-scenarios.md`. For each scenario, paste the **Scenario** text as the contributor's
   message (adopt the stated contributor type where one is given).
3. Compare the skill's actual behavior to **Expected**.
4. A scenario **passes** only if the skilled behavior matches Expected. Record the outcome inline
   under the scenario: `RESULT: pass|fail (YYYY-MM-DD) — notes`.
5. On a **fail**, fix `SKILL.md` or the relevant `references/*.md`, then re-run that scenario.

## Baseline (optional but recommended)

To see a gate's value, run the same scenario **without** the skill first (a fresh session, no
`cae-promoter`) and note the unguided behavior. The gate earns its place if the skilled run differs
in the direction Expected describes.

## Priority set

If you only run a subset, run the highest-value gates first:
**S1, S7, S9, S10a, S10b, S11, S12b, S12c, S13, S14** — the guided probe, brand mechanics,
hard-stop refusal, acts-as-Tenable refusal, promotion-PR-allowed, Hexa truth-check, intake
no-auto-submit, intake choice-mapping, preflight, and promo-clip completeness.

## Scope note

Scenarios are LLM-behavior checks; expect some run-to-run variance. Treat a gate as solid when it
holds across a few reps, not a single lucky pass.
