from pathlib import Path
from scripts.read_vocab import extract_literals

FIXTURE = Path(__file__).parent / "fixtures" / "validator_sample.py"

def test_extracts_integrations_including_multiword():
    vocab = extract_literals(FIXTURE.read_text())
    assert "Tenable Hexa AI MCP" in vocab["integrations"]
    assert "Anthropic" in vocab["integrations"]

def test_extracts_tier_and_platforms():
    vocab = extract_literals(FIXTURE.read_text())
    assert set(vocab["tier"]) == {"contributed", "community-reviewed", "certified"}
    assert "Claude Code" in vocab["compatible_platforms"]

def test_unknown_field_absent_not_crashing():
    vocab = extract_literals(FIXTURE.read_text())
    assert "nonexistent_field" not in vocab

def test_repeated_field_aggregates_not_overwrites():
    # playbook_type is defined 3x in the real validator.py (standard/sponsored/n8n),
    # once per playbook subclass. Members must be UNIONED, not last-write-wins.
    source = (
        'from typing import Literal\n'
        'class A:\n'
        '    playbook_type: Literal["standard"]\n'
        'class B:\n'
        '    playbook_type: Literal["sponsored"]\n'
        'class C:\n'
        '    playbook_type: Literal["n8n"]\n'
    )
    vocab = extract_literals(source)
    assert sorted(vocab["playbook_type"]) == ["n8n", "sponsored", "standard"]


def test_first_seen_order_is_preserved_across_repeated_definitions():
    # The docstring promises first-seen order with new members APPENDED -- never
    # last-write-wins, never re-sorted. The aggregation test above sorts its result,
    # so this is the only test that can see an ordering regression.
    source = (
        'from typing import Literal\n'
        'class A:\n'
        '    tier: Literal["zulu", "alpha"]\n'
        'class B:\n'
        '    tier: Literal["mike", "alpha"]\n'
    )
    # "zulu" before "alpha" (source order, not sorted); "mike" appended; "alpha" not
    # duplicated by the second definition.
    assert extract_literals(source)["tier"] == ["zulu", "alpha", "mike"]
