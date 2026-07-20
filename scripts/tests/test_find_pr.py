import json
from pathlib import Path
from scripts.find_pr import pick_pr_number

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "pr_search_sample.json").read_text())

def test_picks_closed_add_listing_over_open_and_edits_and_issues():
    # #130 open (excluded), #88 closed-but-edit, #12 closed-but-issue(lower!), #59 closed Add-listing wins
    assert pick_pr_number(FIXTURE) == 59

def test_excludes_open_prs():
    data = {"items": [{"number": 41, "title": "Add listing: X", "state": "open", "pull_request": {}}]}
    assert pick_pr_number(data) is None

def test_ignores_non_pr_items_even_if_lower_numbered():
    data = {"items": [
        {"number": 12, "title": "Add listing: X", "state": "closed"},                      # issue, no pull_request
        {"number": 41, "title": "Add listing: X", "state": "closed", "pull_request": {}},   # the real PR
    ]}
    assert pick_pr_number(data) == 41

def test_no_add_listing_falls_back_to_lowest_closed_pr():
    data = {"items": [
        {"number": 90, "title": "docs", "state": "closed", "pull_request": {}},
        {"number": 71, "title": "fix", "state": "closed", "pull_request": {}},
    ]}
    assert pick_pr_number(data) == 71

def test_empty_returns_none():
    assert pick_pr_number({"items": []}) is None
