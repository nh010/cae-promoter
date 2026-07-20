from pathlib import Path
from scripts.scaffold_promo import scaffold, CAPABILITY_FILES

def _assets(tmp_path: Path) -> Path:
    """Build a minimal assets_dir with one recognizable template."""
    a = tmp_path / "assets"
    (a / "copy").mkdir(parents=True)
    (a / "copy" / "linkedin.md").write_text("LINKEDIN TEMPLATE\n")
    (a / "promo-record.template.yaml").write_text("slug: TBD\n")
    (a / "README.template.md").write_text("# Promo bundle\n")
    (a / "value-statements.template.md").write_text("# Value statements\n")
    return a

def test_creates_selected_capability_files(tmp_path):
    assets = _assets(tmp_path)
    repo = tmp_path / "repo"
    repo.mkdir()
    written = scaffold(repo, ["copy", "video"], assets_dir=assets)
    assert "promo/copy/linkedin.md" in written
    assert "promo/video/recording-outline.md" in written
    assert "promo/README.md" in written
    assert "promo/promo-record.yaml" in written
    assert "promo/value-statements.md" in written   # always written (cross-capability)
    # visual-aids NOT selected -> not written
    assert not any(p.startswith("promo/visual-aids/") for p in written)

def test_copies_template_content_when_present(tmp_path):
    assets = _assets(tmp_path)
    repo = tmp_path / "repo"; repo.mkdir()
    scaffold(repo, ["copy"], assets_dir=assets)
    assert (repo / "promo/copy/linkedin.md").read_text() == "LINKEDIN TEMPLATE\n"
    # x.md has no template -> empty stub created
    assert (repo / "promo/copy/x.md").exists()
    assert (repo / "promo/copy/x.md").read_text() == ""

def test_idempotent_does_not_clobber_edited_file(tmp_path):
    assets = _assets(tmp_path)
    repo = tmp_path / "repo"; repo.mkdir()
    scaffold(repo, ["copy"], assets_dir=assets)
    edited = repo / "promo/copy/linkedin.md"
    edited.write_text("MY EDITS")
    written = scaffold(repo, ["copy"], assets_dir=assets)  # second run
    assert edited.read_text() == "MY EDITS"                 # preserved
    assert "promo/copy/linkedin.md" not in written          # reported as skipped

def test_overwrite_true_replaces(tmp_path):
    assets = _assets(tmp_path)
    repo = tmp_path / "repo"; repo.mkdir()
    scaffold(repo, ["copy"], assets_dir=assets)
    (repo / "promo/copy/linkedin.md").write_text("MY EDITS")
    scaffold(repo, ["copy"], assets_dir=assets, overwrite=True)
    assert (repo / "promo/copy/linkedin.md").read_text() == "LINKEDIN TEMPLATE\n"

def test_capability_files_keys():
    assert set(CAPABILITY_FILES) == {"copy", "video", "visual-aids"}
