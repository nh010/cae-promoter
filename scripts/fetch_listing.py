"""Resolve a CyberAgents Exchange listing URL to its metadata dict.

Canonical source: the public content repo frontmatter (uniform across all four listing
types). The /api/*.json endpoints only work for agents and playbooks, so we do not rely
on them here.
"""
import re
import urllib.error
import urllib.request

CONTENT_RAW_BASE = "https://raw.githubusercontent.com/tenable/cyberagents-exchange/main"

# URL type segment (singular or plural) -> content-repo dir (always plural)
_TYPE_MAP = {
    "agent": "agents", "agents": "agents",
    "skill": "skills", "skills": "skills",
    "mcp-server": "mcp-servers", "mcp-servers": "mcp-servers",
    "playbook": "playbooks", "playbooks": "playbooks",
}


def parse_listing_url(url: str) -> tuple[str, str]:
    """Return (listing_type, slug) from an Exchange listing URL."""
    path = re.sub(r"^https?://[^/]+", "", url).strip("/")
    parts = path.split("/")
    if len(parts) < 2 or parts[0] not in _TYPE_MAP:
        raise ValueError(f"Unrecognized Exchange listing URL: {url!r}")
    return _TYPE_MAP[parts[0]], parts[1]


def _coerce(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip('"').strip("'") for p in inner.split(",")]
    low = raw.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    return raw.strip('"').strip("'")


def parse_frontmatter(md: str) -> dict:
    """Parse a leading ---fenced YAML frontmatter block (flat keys only)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", md, re.DOTALL)
    if not m:
        raise ValueError("No frontmatter block found")
    out: dict = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = _coerce(value)
    return out


def fetch_listing(url: str, *, content_base: str = CONTENT_RAW_BASE) -> dict:
    listing_type, slug = parse_listing_url(url)
    raw_url = f"{content_base}/{listing_type}/{slug}.md"
    with urllib.request.urlopen(raw_url, timeout=15) as resp:
        md = resp.read().decode("utf-8")
    fm = parse_frontmatter(md)
    fm["_listing_type"] = listing_type
    fm["_slug"] = slug
    return fm


def resolve_listing(url: str, *, content_base: str = CONTENT_RAW_BASE) -> dict | None:
    """Preflight-friendly wrapper around fetch_listing.

    Returns the listing dict on success, or None when the listing doesn't exist (HTTP 404) so the
    caller has a deterministic stop-and-refer signal instead of a raw traceback. A listing that
    exists but is a seeded example carries `visibility: "example"` in the returned dict — the caller
    must still check that (it's a real listing file, not a 404). Other HTTP/network errors still
    raise, since those are transient/environmental, not "no such listing."
    """
    try:
        return fetch_listing(url, content_base=content_base)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def is_example(listing: dict | None) -> bool:
    """True if the resolved listing is a seeded example (hidden from browse/leaderboard)."""
    return bool(listing) and str(listing.get("visibility", "")).strip().lower() == "example"


if __name__ == "__main__":
    import json
    import sys
    result = resolve_listing(sys.argv[1])
    if result is None:
        print("NOT_FOUND — no such listing; refer the contributor to cyberagents-exchange-submit")
        raise SystemExit(2)
    if is_example(result):
        print("EXAMPLE_SEED — this is a seeded example listing (visibility: example); "
              "refer the contributor to cyberagents-exchange-submit")
        raise SystemExit(3)
    print(json.dumps(result, indent=2, default=str))
