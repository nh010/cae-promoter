"""Extract controlled-vocabulary Literal enums from the Exchange validator.py source."""
import ast
import urllib.request

VALIDATOR_URL = "https://raw.githubusercontent.com/tenable/cyberagents-exchange/main/validator.py"


def _literal_members(node: ast.AST) -> list[str] | None:
    """If node is a Literal[...] subscript, return its string members, else None."""
    if not isinstance(node, ast.Subscript):
        return None
    base = node.value
    if not (isinstance(base, ast.Name) and base.id == "Literal"):
        return None
    sl = node.slice
    elts = sl.elts if isinstance(sl, ast.Tuple) else [sl]
    members = [e.value for e in elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return members or None


def extract_literals(source: str) -> dict[str, list[str]]:
    """Map each annotated field name to its Literal string members.

    Handles both `field: Literal[...]` and `field: list[Literal[...]]`.
    Members are UNIONED across repeated field definitions (e.g. `playbook_type`
    is declared once per playbook subclass), preserving first-seen order and
    appending any new members — never last-write-wins.
    """
    tree = ast.parse(source)
    out: dict[str, list[str]] = {}
    for ann in ast.walk(tree):
        if not isinstance(ann, ast.AnnAssign) or not isinstance(ann.target, ast.Name):
            continue
        field = ann.target.id
        # direct Literal[...]
        members = _literal_members(ann.annotation)
        # list[Literal[...]]  -> unwrap the subscript's slice
        if members is None and isinstance(ann.annotation, ast.Subscript):
            members = _literal_members(ann.annotation.slice)
        if members:
            existing = out.setdefault(field, [])
            for m in members:
                if m not in existing:
                    existing.append(m)
    return out


def fetch_vocab(url: str = VALIDATOR_URL) -> dict[str, list[str]]:
    with urllib.request.urlopen(url, timeout=15) as resp:
        source = resp.read().decode("utf-8")
    return extract_literals(source)


if __name__ == "__main__":
    import json
    print(json.dumps(fetch_vocab(), indent=2))
