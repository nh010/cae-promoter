import subprocess
import sys
from pathlib import Path

import pytest

from scripts._http import ENV_VAR, FETCH_TIMEOUT, SEARCH_TIMEOUT, timeout_seconds

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_default_is_returned_when_unset(monkeypatch):
    monkeypatch.delenv(ENV_VAR, raising=False)
    assert timeout_seconds(FETCH_TIMEOUT) == FETCH_TIMEOUT
    assert timeout_seconds(SEARCH_TIMEOUT) == SEARCH_TIMEOUT


def test_an_empty_value_means_unset_not_error(monkeypatch):
    monkeypatch.setenv(ENV_VAR, "   ")
    assert timeout_seconds(FETCH_TIMEOUT) == FETCH_TIMEOUT


def test_a_valid_override_wins(monkeypatch):
    monkeypatch.setenv(ENV_VAR, "45")
    assert timeout_seconds(FETCH_TIMEOUT) == 45.0


def test_junk_raises_rather_than_silently_defaulting(monkeypatch):
    # The whole point of the override is that the operator can tell it took effect.
    # Falling back to the default here would answer "nothing" while looking like it
    # answered "something".
    monkeypatch.setenv(ENV_VAR, "thirty")
    with pytest.raises(ValueError, match="is not a number"):
        timeout_seconds(FETCH_TIMEOUT)


@pytest.mark.parametrize("bad", ["0", "-5"])
def test_a_non_positive_override_raises(monkeypatch, bad):
    monkeypatch.setenv(ENV_VAR, bad)
    with pytest.raises(ValueError, match="greater than 0"):
        timeout_seconds(FETCH_TIMEOUT)


@pytest.mark.parametrize("module", ["read_vocab", "fetch_listing", "find_pr"])
def test_each_script_still_imports_when_run_directly(module):
    """SKILL.md tells Claude to run these as `python3 scripts/<name>.py`.

    That puts scripts/ on sys.path[0], where the shared helper is top-level `_http`
    rather than `scripts._http`. A single package-style import would satisfy pytest
    and break every documented invocation, so pin both modes: pytest covers the
    package path by importing scripts.* above, and this covers direct execution by
    importing with scripts/ as the working directory.
    """
    proc = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        cwd=REPO_ROOT / "scripts", capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
