"""Shared HTTP timeout policy for this skill's network helpers.

Every outbound call in the package resolves its timeout through `timeout_seconds()`,
so a contributor on a slow link raises them all in one place instead of editing three
scripts.

Env override: `CAE_PROMOTER_HTTP_TIMEOUT`, in seconds, greater than zero.

An unusable override **raises** rather than quietly falling back to the default. An
operator who exports the variable and silently gets the default anyway has no way to
tell their setting did nothing -- the same failure family as a checker that substitutes
a default for a missing dependency and reports "nothing" as though it were "something."
An unset or empty value is not an error; it just means "use the default."
"""
import os

ENV_VAR = "CAE_PROMOTER_HTTP_TIMEOUT"

# Defaults per call class: a raw single-file GET is quick, a search round trip is not.
FETCH_TIMEOUT = 15.0   # raw.githubusercontent.com file GET (fetch_listing, read_vocab)
SEARCH_TIMEOUT = 20.0  # GitHub search API and the `gh` subprocess (find_pr)


def timeout_seconds(default: float) -> float:
    """Resolve an urllib/subprocess timeout, honouring the env override."""
    raw = os.environ.get(ENV_VAR)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = float(raw)
    except ValueError:
        raise ValueError(f"{ENV_VAR}={raw!r} is not a number") from None
    if value <= 0:
        raise ValueError(f"{ENV_VAR}={raw!r} must be greater than 0")
    return value
