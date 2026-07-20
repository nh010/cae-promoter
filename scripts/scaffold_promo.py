"""Create the promo/ bundle tree for the selected capabilities.

Copies skeleton templates from an assets_dir when present; otherwise writes empty stubs.
Idempotent by default (never clobbers an existing file unless overwrite=True).
"""
from pathlib import Path

CAPABILITY_FILES: dict[str, list[str]] = {
    "copy": ["copy/linkedin.md", "copy/x.md", "copy/slack.md", "copy/listing-section.md"],
    "video": ["video/recording-outline.md"],
    "visual-aids": ["visual-aids/diagram-spec.md", "visual-aids/screenshot-guide.md", "visual-aids/card.md"],
}

# Always-written files: (output path under promo/, template filename in assets_dir)
_ALWAYS = [
    ("value-statements.md", "value-statements.template.md"),
    ("README.md", "README.template.md"),
    ("promo-record.yaml", "promo-record.template.yaml"),
]


def _write(dst: Path, template: Path | None, overwrite: bool) -> bool:
    """Write dst from template (or empty). Return True if written, False if skipped."""
    if dst.exists() and not overwrite:
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(template.read_text() if template and template.exists() else "")
    return True


def scaffold(repo_root, capabilities, *, assets_dir, overwrite: bool = False) -> list[str]:
    repo_root = Path(repo_root)
    assets_dir = Path(assets_dir)
    promo = repo_root / "promo"
    written: list[str] = []

    for out_name, tpl_name in _ALWAYS:
        if _write(promo / out_name, assets_dir / tpl_name, overwrite):
            written.append(f"promo/{out_name}")

    for cap in capabilities:
        for rel in CAPABILITY_FILES.get(cap, []):
            # template mirrors the output path under assets_dir (e.g. assets/copy/linkedin.md)
            if _write(promo / rel, assets_dir / rel, overwrite):
                written.append(f"promo/{rel}")

    return sorted(written)


if __name__ == "__main__":
    import sys
    root, *caps = sys.argv[1:]
    here = Path(__file__).resolve().parent.parent / "assets"
    for p in scaffold(root, caps, assets_dir=here):
        print(p)
