"""Assemble a pre-filled CyberAgents Exchange intake-form URL from a field->value dict.

Pure and offline: it only string-builds (no network, no Forms API). The entry.<id> map, exact
choice-option strings, and viewform base are the source of truth in docs/intake-form-fields.md
(live re-extract 2026-07-20, 24 fields); this module encodes that map and is the one place to
update if the form changes.

Two rules make Google Forms pre-fill actually populate a field:
  1. a choice value must EXACTLY match a listed option string (case/punctuation/parens/dashes), and
  2. every value is URL-encoded.

Choice handling:
  - region / industry are free-form demographics -> support Google's two-param "Other" mechanism
    (entry.<id>=__other_option__ & entry.<id>.other_option_response=<text>) for off-list values.
  - contributor_type / build_type / social_tag_optin / future_outreach are LOCKED: the skill always
    holds a known listed value (type from interview, build from ingest, opt-ins are Yes/No). Even
    though the live form now exposes "Other" on the first three, an unmatched value here is a skill
    bug, so build() RAISES rather than silently routing to "Other."
"""
import urllib.parse

VIEWFORM_BASE = "https://docs.google.com/forms/d/e/1FAIpQLSf27i8jsPMbIwtp4FFHBd3F5RBHGXK-65ONDB7O0VHFMC16kw/viewform"

# field key -> entry.<id> (form order; see docs/intake-form-fields.md)
ENTRY = {
    "name": "entry.1596500923",
    "work_email": "entry.1580263152",
    "contributor_type": "entry.1899964244",
    "job_title": "entry.34266064",
    "organization": "entry.1135422228",
    "org_size": "entry.1236656087",
    "security_team_size": "entry.1678117250",
    "region": "entry.1880062348",
    "industry": "entry.1581560595",
    "asset_name": "entry.1153617233",
    "build_type": "entry.1563284810",
    "listing_url": "entry.546272964",
    "repo_url": "entry.80140529",
    "value_1": "entry.1167207484",
    "value_2": "entry.1470473782",
    "value_3": "entry.415351116",
    "social_tag_optin": "entry.1985420160",
    "x_twitter": "entry.1079612501",
    "bluesky": "entry.2085830831",
    "linkedin": "entry.1615438749",
    "reddit": "entry.859295616",
    "github_handle": "entry.1037521172",
    "other_social": "entry.1278806003",
    "future_outreach": "entry.963519517",
}

# Exact option strings per choice field (verbatim from the live form).
OPTIONS = {
    "contributor_type": ["Community contributor", "Tenable employee", "Tenable partner"],
    "region": [
        "Asia-Pacific (incl. Australia and New Zealand)",
        "Europe",
        "Latin America (Mexico, Central, and South America)",
        "North America (US, Canada)",
        "Middle East and Africa",
    ],
    "industry": [
        "Education",
        "Financial institutions and insurance",
        "Government and public sector",
        "Healthcare and life sciences",
        "Manufacturing and industrial",
        "Retail and e-commerce",
        "Technology and software",
        "Telecommunications and media",
    ],
    "build_type": ["Agent", "Skill", "MCP Server", "Playbook"],
    "social_tag_optin": ["Yes", "No"],
    "future_outreach": ["Yes", "No"],
}

# Choice fields that accept a custom "Other" value (the only genuinely free-form demographics).
OTHER_OK = {"region", "industry"}


def _pairs(field: str, value: str) -> list[tuple[str, str]]:
    """Return the entry pair(s) for one field. Choice fields validate; region/industry may 'Other'."""
    entry = ENTRY[field]
    if field in OPTIONS:
        if value in OPTIONS[field]:
            return [(entry, value)]
        if field in OTHER_OK:
            return [(entry, "__other_option__"), (f"{entry}.other_option_response", value)]
        raise ValueError(
            f"{field}={value!r} is not a listed option {OPTIONS[field]} and {field} has no 'Other' path"
        )
    return [(entry, value)]


def build(values: dict) -> str:
    """Build the pre-filled viewform URL. Drops empty/None values; raises on an unknown field key
    or an unmatched value on a locked choice field."""
    parts: list[str] = []
    for field, value in values.items():
        if field not in ENTRY:
            raise ValueError(f"Unknown intake field: {field!r}")
        if value is None or value == "":
            continue
        for key, val in _pairs(field, str(value)):
            parts.append(f"{key}={urllib.parse.quote_plus(val)}")
    return f"{VIEWFORM_BASE}?{'&'.join(parts)}"


if __name__ == "__main__":
    import json
    import sys
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(build(json.loads(raw)))
