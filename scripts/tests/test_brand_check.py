from scripts.brand_check import check, Finding

# --- straight quotes ---
def test_flags_straight_double_quote():
    fs = check('He said "hello" today.', channel="linkedin")
    assert any(f.rule == "straight-quote" for f in fs)

def test_flags_straight_single_quote_apostrophe():
    fs = check("it's a great tool", channel="linkedin")
    assert any(f.rule == "straight-quote" for f in fs)

def test_smart_quotes_pass():
    fs = check("it’s a “great” tool", channel="linkedin")
    assert not any(f.rule == "straight-quote" for f in fs)

# --- em-dash cap (short-form) ---
def test_short_form_one_em_dash_ok():
    fs = check("Cut triage 70% — measured across incidents.", channel="x")
    assert not any(f.rule == "em-dash-cap" for f in fs)

def test_short_form_two_em_dashes_flagged():
    fs = check("Cut triage — fast — and clean.", channel="linkedin")
    assert any(f.rule == "em-dash-cap" for f in fs)

def test_long_form_em_dashes_not_capped():
    # listing/readme is long-form: minimize, don't count — no em-dash-cap finding
    fs = check("A — B — C — D.", channel="listing")
    assert not any(f.rule == "em-dash-cap" for f in fs)

# --- X length ---
def test_x_over_280_flagged():
    fs = check("x" * 281, channel="x")
    assert any(f.rule == "x-length" for f in fs)

def test_x_at_280_ok():
    fs = check("x" * 280, channel="x")
    assert not any(f.rule == "x-length" for f in fs)

def test_length_not_checked_off_x():
    fs = check("x" * 500, channel="linkedin")
    assert not any(f.rule == "x-length" for f in fs)

# --- banned abbreviations ---
def test_banned_abbreviation_flagged():
    fs = check("Our TVM tool scans everything.", channel="linkedin")
    assert any(f.rule == "banned-abbreviation" and "TVM" in f.detail for f in fs)

def test_abbreviation_word_boundary_no_false_positive():
    # "was" the ordinary word must not trip the WAS product-abbrev rule
    fs = check("It was fast.", channel="linkedin")
    assert not any(f.rule == "banned-abbreviation" for f in fs)

def test_tenable_io_flagged():
    fs = check("Tenable.io is great", channel="linkedin")
    assert any(f.rule == "banned-abbreviation" for f in fs)

# --- banned phrases ---
def test_banned_phrase_flagged():
    fs = check("We eliminate risk for you.", channel="linkedin")
    assert any(f.rule == "banned-phrase" for f in fs)

def test_on_premise_flagged():
    fs = check("Runs on-premise today.", channel="linkedin")
    assert any(f.rule == "on-premise" for f in fs)

def test_on_premises_ok():
    fs = check("Runs on-premises today.", channel="linkedin")
    assert not any(f.rule == "on-premise" for f in fs)

# --- HTML comments (template guidance) are ignored ---
def test_comment_content_not_flagged():
    # A skeleton's instructional comment names banned abbreviations + uses a straight quote as an
    # example; none of that is published copy, so it must not trip findings.
    templated = '<!-- never use VM/RBVM/Tenable.io; smart quotes not "straight" -->\nReal copy here.'
    assert check(templated, channel="linkedin") == []

def test_real_text_outside_comment_still_flagged():
    templated = '<!-- guidance -->\nOur TVM tool "rocks".'
    fs = check(templated, channel="linkedin")
    assert any(f.rule == "banned-abbreviation" for f in fs)
    assert any(f.rule == "straight-quote" for f in fs)

def test_angle_bracket_placeholders_ignored():
    # a skeleton fill-in prompt with an em dash + apostrophe inside is scaffolding, not copy
    tmpl = "<the metric — saved / triaged — who it's for>\n\nReal clean copy."
    assert check(tmpl, channel="linkedin") == []

def test_real_em_dashes_still_counted_outside_placeholders():
    # two real em dashes in actual short-form copy must still trip the cap
    fs = check("Cut triage — fast — clean.", channel="x")
    assert any(f.rule == "em-dash-cap" for f in fs)

# --- clean copy passes ---
def test_clean_short_form_no_findings():
    clean = "We cut triage time about 70%. It’s free on the Exchange."
    assert check(clean, channel="x") == []

# --- Finding shape ---
def test_finding_is_namedtuple_like():
    f = check('"x"', channel="x")[0]
    assert isinstance(f, Finding)
    assert hasattr(f, "rule") and hasattr(f, "detail")
