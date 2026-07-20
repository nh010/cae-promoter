"""Deterministic brand-mechanics linter for generated promo copy.

Catches the high-frequency, mechanical brand failures a human/model eyeball misses: straight quotes,
the one-em-dash short-form cap, the X 280-char limit, banned product-name abbreviations, and banned
phrases. This is the tool Gate 3 (brand + legal) runs so the check is deterministic, not vibes. It
does NOT replace judgment calls (voice/attribution, customer-name flags) — it covers the mechanics.

Usage (fast path for the skill):
    python scripts/brand_check.py <channel> <file>      # or pipe text on stdin
    channel ∈ {x, twitter, linkedin, slack, listing, readme, other}
Exit 0 = clean, 1 = findings printed (one per line).
"""
import re
import sys
from typing import NamedTuple


class Finding(NamedTuple):
    rule: str
    detail: str


# Short-form channels: hard cap of ONE em dash. Long-form: minimize, don't count.
_SHORT_FORM = {"x", "twitter", "linkedin", "slack"}
_X_LIMIT = 280

# Banned product-name abbreviations (word-boundary matched so "was" the word is safe).
_BANNED_ABBREV = ["RBVM", "TVM", "VM", "WAS", ".asm", ".cs"]
# Tenable.io / Tenable.cs style dotted product names.
_TENABLE_DOTTED = re.compile(r"\bTenable\.(io|asm|cs)\b", re.IGNORECASE)

# Banned filler / off-message phrases (substring, case-insensitive).
_BANNED_PHRASES = [
    "eliminate risk",
    "eliminate exposures",
    "eradicate exposures",
    "legacy vulnerabilities",
    "cyber exposure",
]


def _abbrev_pattern(abbrev: str) -> re.Pattern:
    # `.asm`/`.cs` start with a dot; guard the trailing boundary only. Others: full word boundary.
    if abbrev.startswith("."):
        return re.compile(re.escape(abbrev) + r"\b")
    return re.compile(r"\b" + re.escape(abbrev) + r"\b")


_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# Skeleton fill-in prompts: <hook: ...>, <one CTA: link>, <asset name>. Always a single
# angle-bracketed span with no line break — the contributor replaces the whole token, so its
# guidance text (which can contain example dashes/apostrophes) is not published copy.
_PLACEHOLDER = re.compile(r"<[^<>\n]+>")


def check(text: str, *, channel: str = "other") -> list[Finding]:
    """Return brand-mechanics findings for `text` on the given channel. Empty list = clean.

    Template scaffolding is stripped before checking so the linter runs cleanly on a still-templated
    file and only flags real, contributor-visible copy: HTML comments (`<!-- ... -->`, which carry
    brand-rule reminders that name banned abbreviations and use quotes as examples) and `<...>`
    fill-in prompts (which the contributor replaces wholesale).
    """
    ch = channel.lower()
    text = _COMMENT.sub("", text)
    text = _PLACEHOLDER.sub("", text)
    findings: list[Finding] = []

    # Straight quotes (double or single/apostrophe) — always a violation in published copy.
    if '"' in text:
        findings.append(Finding("straight-quote", 'straight double quote " — use “ ”'))
    if "'" in text:
        findings.append(Finding("straight-quote", "straight single quote ' — use ‘ ’ or ’"))

    # Em-dash cap on short-form only.
    if ch in _SHORT_FORM:
        n = text.count("—")
        if n > 1:
            findings.append(Finding("em-dash-cap", f"{n} em dashes in short-form (cap is 1)"))

    # X length.
    if ch in {"x", "twitter"} and len(text) > _X_LIMIT:
        findings.append(Finding("x-length", f"{len(text)} chars (X limit is {_X_LIMIT})"))

    # Banned abbreviations (word-boundary) + dotted product names.
    for ab in _BANNED_ABBREV:
        if _abbrev_pattern(ab).search(text):
            findings.append(Finding("banned-abbreviation", f"{ab} — spell out the full product name"))
    if _TENABLE_DOTTED.search(text):
        findings.append(Finding("banned-abbreviation", "Tenable.<x> — spell out the full product name"))

    # on-premise (wrong word) vs on-premises.
    if re.search(r"\bon-premise\b", text, re.IGNORECASE):
        findings.append(Finding("on-premise", 'use "on-premises" (or "on-prem"), never "on-premise"'))

    # Banned phrases.
    low = text.lower()
    for phrase in _BANNED_PHRASES:
        if phrase in low:
            findings.append(Finding("banned-phrase", f'avoid "{phrase}"'))

    return findings


if __name__ == "__main__":
    channel = sys.argv[1] if len(sys.argv) > 1 else "other"
    text = (open(sys.argv[2]).read() if len(sys.argv) > 2 else sys.stdin.read())
    results = check(text, channel=channel)
    if not results:
        print(f"brand check clean ({channel})")
        raise SystemExit(0)
    for f in results:
        print(f"[{f.rule}] {f.detail}")
    raise SystemExit(1)
