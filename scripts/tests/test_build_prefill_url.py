import urllib.parse
import pytest
from scripts.build_prefill_url import build, VIEWFORM_BASE, ENTRY, OPTIONS, OTHER_OK


def _params(url):
    """Parse the query into a decoded {param: value} dict."""
    assert url.startswith(VIEWFORM_BASE + "?")
    query = url[len(VIEWFORM_BASE) + 1:]
    return dict(urllib.parse.parse_qsl(query, keep_blank_values=True))


def test_base_and_encoding():
    url = build({"name": "Ada Lovelace", "value_1": "cut triage 45m -> 8m; killed #1 pain & saved 10h/wk"})
    assert url.startswith(VIEWFORM_BASE + "?")
    query = url.split("?", 1)[1]
    assert "%23" in query                      # '#' escaped
    assert "%26" in query                      # '&' inside a value escaped, never a bare separator
    assert "+" in query or "%20" in query      # space escaped
    params = _params(url)                       # and it all round-trips
    assert params["entry.1596500923"] == "Ada Lovelace"
    assert params["entry.1167207484"].startswith("cut triage")
    assert "#1 pain & saved" in params["entry.1167207484"]


def test_entry_id_mapping():
    assert ENTRY["name"] == "entry.1596500923"
    assert ENTRY["value_1"] == "entry.1167207484"
    assert ENTRY["work_email"] == "entry.1580263152"
    # new 2026-07-20 social block
    assert ENTRY["social_tag_optin"] == "entry.1985420160"
    assert ENTRY["linkedin"] == "entry.1615438749"
    assert ENTRY["github_handle"] == "entry.1037521172"


def test_choice_exact_match_plain_param():
    url = build({"contributor_type": "Tenable partner", "region": "Europe",
                 "industry": "Technology and software", "build_type": "MCP Server",
                 "social_tag_optin": "Yes", "future_outreach": "No"})
    params = _params(url)
    assert params["entry.1899964244"] == "Tenable partner"
    assert params["entry.1880062348"] == "Europe"
    assert params["entry.1581560595"] == "Technology and software"
    assert params["entry.1563284810"] == "MCP Server"
    assert params["entry.1985420160"] == "Yes"
    assert params["entry.963519517"] == "No"


def test_locked_choices_unmatched_raise():
    # contributor_type + build_type expose "Other" on the form, but the skill always holds a
    # listed value; an unmatched value is a bug we surface by raising, not silently "Other"-ing.
    with pytest.raises(ValueError):
        build({"contributor_type": "Freelancer"})
    with pytest.raises(ValueError):
        build({"build_type": "Extension"})
    with pytest.raises(ValueError):
        build({"future_outreach": "Maybe"})


def test_region_industry_other_two_param():
    url = build({"region": "Antarctica", "industry": "Aerospace and defense"})
    params = _params(url)
    assert params["entry.1880062348"] == "__other_option__"
    assert params["entry.1880062348.other_option_response"] == "Antarctica"
    assert params["entry.1581560595"] == "__other_option__"
    assert params["entry.1581560595.other_option_response"] == "Aerospace and defense"


def test_optional_fields_omitted_when_empty():
    url = build({"name": "X", "value_2": "", "value_3": None, "github_handle": ""})
    params = _params(url)
    assert "entry.1596500923" in params
    assert "entry.1470473782" not in params     # value_2 empty
    assert "entry.415351116" not in params       # value_3 None
    assert "entry.1037521172" not in params       # github_handle empty


def test_size_passthrough_specific_and_range():
    url = build({"org_size": "4200", "security_team_size": "5,001–25,000"})
    params = _params(url)
    assert params["entry.1236656087"] == "4200"
    assert params["entry.1678117250"] == "5,001–25,000"   # en dash + comma survive round-trip


def test_social_handles_optional_passthrough_and_omit():
    url = build({"social_tag_optin": "Yes", "x_twitter": "@ada", "bluesky": "",
                 "linkedin": "in/ada", "reddit": None,
                 "other_social": "mastodon: @ada@infosec.exchange"})
    params = _params(url)
    assert params["entry.1985420160"] == "Yes"
    assert params["entry.1079612501"] == "@ada"
    assert params["entry.1615438749"] == "in/ada"
    assert params["entry.1278806003"].startswith("mastodon")
    assert "entry.2085830831" not in params     # bluesky empty
    assert "entry.859295616" not in params        # reddit None


def test_other_ok_is_region_and_industry_only():
    assert OTHER_OK == {"region", "industry"}
