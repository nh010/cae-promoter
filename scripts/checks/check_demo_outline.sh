#!/usr/bin/env bash
# Guards the demo outline's five beats, its stated duration target, and its hard cap.
#
# Why this exists: the outline's structure and its numbers live in PROSE at four sites
# (the capability reference, the contributor-facing template, the handoff coaching step,
# and the bundle README template). Nothing else in this repo can see a site left at an
# old number, and the failure is silent -- the skill just coaches the old structure.
#
# Exit codes:
#   0  every invariant holds
#   1  at least one invariant failed (a real finding)
#   2  nothing was checked (a guarded file is missing) -- never read this as a pass
set -uo pipefail

SK=$(cd "$(dirname "$0")/../.." && pwd)   # skill root from THIS script's location,
                                          # never a hardcoded installed path: a
                                          # hardcoded root grades the installed tree
                                          # while the edit under review sits elsewhere.
REF="$SK/references/capability-video.md"
TPL="$SK/assets/video/recording-outline.md"
HANDOFF="$SK/references/handoff.md"
BUNDLE_README="$SK/assets/README.template.md"

for f in "$REF" "$TPL" "$HANDOFF" "$BUNDLE_README"; do
  [ -f "$f" ] || { echo "NOTHING CHECKED: missing $f"; exit 2; }
done

fail=0
note() { echo "FAIL: $1"; fail=1; }

# --- The five beats, in order, in both the reference and the template ---
BEATS=("Intro" "Elevator pitch" "Demo" "Setup / config" "CTA")
for b in "${BEATS[@]}"; do
  grep -qF "$b" "$TPL" || note "template is missing beat '$b'"
  grep -qF "$b" "$REF" || note "reference is missing beat '$b'"
done

# Beat order in the template must match BEATS. Compare the beat headings only
# (lines starting with '- **'), so prose mentioning a beat name cannot reorder this.
got=$(grep -oE '^- \*\*(Intro|Elevator pitch|Demo|Setup / config|CTA)' "$TPL" \
        | sed 's/^- \*\*//')
want=$(printf '%s\n' "${BEATS[@]}")
[ "$got" = "$want" ] || note "template beat order is not Intro/Elevator pitch/Demo/Setup / config/CTA (got: $(echo "$got" | tr '\n' ',' ))"

# --- The old five beats must be GONE (clock-anchored, so the plain words
# --- "Problem"/"Value" surviving as vocabulary is not a false positive) ---
for old in 'Problem (~0:00' 'What it does (~0:20' 'Install / config (~0:50' 'Value (~1:30' 'Where to get it (~2:30'; do
  grep -qF "$old" "$TPL" && note "template still carries the OLD beat '$old'"
done
grep -qF 'Problem → what it does → install/config → value → where to get it' "$REF" \
  && note "reference still carries the OLD beat chain"

# --- The elevator pitch must mandate a value metric OR anecdote ---
# Flattened first: the requirement is one sentence in the prose but wraps across lines
# in the reference, and a line-at-a-time grep would miss it and read as a regression.
flat() { tr '\n' ' ' < "$1" | tr -s ' '; }
for f in "$REF" "$TPL"; do
  flat "$f" | grep -qiE 'value metric.*(or|/).*(value )?anecdote' \
    || note "$(basename "$f") does not require a value metric or anecdote in the pitch"
done

# --- Duration: 2-3 min stays the stated TARGET, 4:00 is the HARD CAP ---
# The cap must appear at every site that coaches recording; a site left without it
# is exactly the "one of six sites at the old number" failure this rule guards.
for f in "$REF" "$TPL" "$HANDOFF" "$BUNDLE_README"; do
  grep -qE 'never (run |go )?(longer|over) than four minutes|hard cap|4:00' "$f" \
    || note "$(basename "$f") does not state the four-minute hard cap"
done
grep -qF '2–3 min' "$REF" || note "reference dropped the 2-3 min target"
grep -qF '2–3 min' "$TPL" || note "template dropped the 2-3 min target"

# --- The clocks must actually fit: last beat's end <= 4:00, and the run should
# --- land inside the stated 2-3 min target rather than at the cap.
last=$(grep -oE '\(~[0-9]+:[0-9]{2}.[0-9]+:[0-9]{2}\)' "$TPL" | tail -1 \
         | grep -oE '[0-9]+:[0-9]{2}' | tail -1)
[ -n "$last" ] || note "could not read the final beat clock from the template"
if [ -n "$last" ]; then
  secs=$(( ${last%%:*} * 60 + ${last##*:} ))
  [ "$secs" -le 240 ] || note "beats run to $last, past the 4:00 hard cap"
  [ "$secs" -le 180 ] || note "beats run to $last, past the 3:00 target top (cap is for overage, not the plan)"
fi

if [ "$fail" -eq 0 ]; then
  echo "OK: five beats in order, old beats gone, metric-or-anecdote required, 2-3 min target + 4:00 cap at all 4 sites, clocks land at ${last:-?}"
  exit 0
fi
exit 1
