# Prose checks

Tests cover this skill's scripts; nothing covers its **prose**. These checks close that gap.
Each one greps the prose for the exact clauses it must contain and the clauses it must not,
and derives the skill root from its own location so it grades the tree it lives in rather
than whatever happens to be installed at `~/.claude/skills/cae-promoter`.

Exit codes are uniform: `0` clean, `1` a real finding, **`2` nothing was checked** (a guarded
file is missing) — never read `2` as a pass.

| Check | Guards |
|---|---|
| `check_demo_outline.sh` | The demo's five beats (intro → elevator pitch → demo → setup / config tips → CTA), in that order, in both `references/capability-video.md` and `assets/video/recording-outline.md`; the absence of the five superseded beats; the mandatory value-metric-or-anecdote in the elevator pitch; and the duration contract — a stated 2–3 min target plus the 4:00 hard cap, at all four sites that coach recording (capability reference, outline template, `references/handoff.md`, `assets/README.template.md`). Also asserts the template's clocks land inside the target rather than at the cap, and cross-checks the clocks between the two files: each beat's reference **duration** must equal its template **span**, the spans must be contiguous from 0:00 with no gap or overlap, and the durations must sum to the final clock. |

Run them all:

```bash
for c in scripts/checks/check_*.sh; do "$c" || echo "FINDING in $c"; done
```
