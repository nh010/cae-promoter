import urllib.error
from pathlib import Path
import pytest
from scripts import fetch_listing as fl
from scripts.fetch_listing import (
    parse_listing_url,
    parse_frontmatter,
    resolve_listing,
    is_example,
)

FIXTURE = (Path(__file__).parent / "fixtures" / "listing_sample.md").read_text()


def _http_error(code):
    return urllib.error.HTTPError(url="x", code=code, msg="e", hdrs=None, fp=None)

def test_parse_url_plural_type_and_slug():
    assert parse_listing_url("https://exchange.tenable.com/skills/cyberagents-exchange-submit") == ("skills", "cyberagents-exchange-submit")

def test_parse_url_singular_type_normalized_to_plural():
    assert parse_listing_url("https://exchange.tenable.com/skill/foo-bar/") == ("skills", "foo-bar")

def test_parse_url_agents_and_mcp():
    assert parse_listing_url("https://exchange.tenable.com/agents/x") == ("agents", "x")
    assert parse_listing_url("https://exchange.tenable.com/mcp-servers/y") == ("mcp-servers", "y")

def test_parse_url_rejects_unknown():
    with pytest.raises(ValueError):
        parse_listing_url("https://exchange.tenable.com/about")

def test_frontmatter_strings_lists_and_bools():
    fm = parse_frontmatter(FIXTURE)
    assert fm["name"] == "CyberAgents Exchange Submit"
    assert fm["tags"] == ["claude-code", "exchange", "submission", "automation", "cybersecurity"]
    assert fm["integrations"] == ["Anthropic"]
    assert fm["compatible_platforms"] == ["Claude Code"]
    assert fm["works_with_tenable_hexa_mcp"] is False
    assert fm["invocation"] == "/cyberagents-exchange-submit"

def test_frontmatter_missing_block_raises():
    with pytest.raises(ValueError):
        parse_frontmatter("no frontmatter here")


def test_resolve_listing_returns_none_on_404(monkeypatch):
    def boom(url, **kw):
        raise _http_error(404)
    monkeypatch.setattr(fl, "fetch_listing", boom)
    assert resolve_listing("https://exchange.tenable.com/skills/nope") is None


def test_resolve_listing_reraises_non_404(monkeypatch):
    def boom(url, **kw):
        raise _http_error(503)
    monkeypatch.setattr(fl, "fetch_listing", boom)
    with pytest.raises(urllib.error.HTTPError):
        resolve_listing("https://exchange.tenable.com/skills/x")


def test_resolve_listing_passes_through_success(monkeypatch):
    monkeypatch.setattr(fl, "fetch_listing", lambda url, **kw: {"name": "X", "_slug": "x"})
    assert resolve_listing("https://exchange.tenable.com/skills/x")["name"] == "X"


def test_is_example_detects_seed():
    assert is_example({"visibility": "example"}) is True
    assert is_example({"visibility": "Example"}) is True   # case-insensitive
    assert is_example({"name": "real"}) is False            # no visibility key
    assert is_example(None) is False                        # not-found never counts as a seed
