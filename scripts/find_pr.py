"""Resolve a contributor's ACCEPTED submission PR number in the Exchange content repo.

An accepted listing = a CLOSED "Add listing: <Name>" PR. Search by the display NAME in the title
first (submission PR titles use the name, not the slug), then fall back to the slug. Among matches,
the LOWEST number is the original submission (later PRs are edits). Prefers the gh CLI
(authenticated, higher search rate limit); falls back to unauthenticated urllib. Returns None when
nothing resolves so the skill can ask the contributor to paste the number.
"""
import json
import shutil
import subprocess
import urllib.parse
import urllib.request

REPO = "tenable/cyberagents-exchange"
SEARCH_URL = "https://api.github.com/search/issues"


def pick_pr_number(search_json: dict) -> int | None:
    """From a /search/issues response, pick the accepted submission PR number.

    Only CLOSED PR items (a 'pull_request' key + state 'closed') qualify — a closed listing PR is
    what marks an accepted asset. Prefer 'Add listing...' titles; among the pool the lowest number
    is the earliest submission (later ones are edits). Return None if nothing qualifies.
    """
    prs = [
        it for it in search_json.get("items", [])
        if "pull_request" in it and it.get("state") == "closed"
    ]
    if not prs:
        return None
    add = [it for it in prs if str(it.get("title", "")).lower().startswith("add listing")]
    pool = add or prs
    return min(pool, key=lambda it: it["number"])["number"]


def _search(query: str) -> dict:
    """Run the GitHub issue search: gh if available, else unauthenticated urllib."""
    if shutil.which("gh"):
        try:
            out = subprocess.run(
                ["gh", "api", "-X", "GET", "/search/issues", "-f", f"q={query}"],
                capture_output=True, text=True, timeout=20, check=True,
            ).stdout
            return json.loads(out)
        except (subprocess.SubprocessError, json.JSONDecodeError):
            pass  # fall through to urllib
    url = f"{SEARCH_URL}?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_pr(name: str, slug: str, *, repo: str = REPO) -> int | None:
    """Search by display name (in title) first, then by slug. Return the accepted PR number or None."""
    queries = [
        f'repo:{repo} type:pr state:closed in:title "{name}"',
        f"repo:{repo} type:pr state:closed {slug}",
    ]
    for q in queries:
        try:
            n = pick_pr_number(_search(q))
        except Exception:
            n = None
        if n is not None:
            return n
    return None


if __name__ == "__main__":
    import sys
    name, slug = sys.argv[1], sys.argv[2]
    n = find_pr(name, slug)
    print(f"#{n}" if n else "NOT FOUND — ask the contributor to paste their PR number")
