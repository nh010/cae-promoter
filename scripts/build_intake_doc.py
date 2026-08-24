#!/usr/bin/env python3
"""Populate the CAE Promoter intake-form build-spec Google Doc.

Builds a structured block list (heading / body / bullet), inserts all text in a
single ordered pass, then applies paragraph styles (named styles + bullets) by
computed character ranges. Text is inserted at index 1 for each block in order,
so we track a running cursor and record each block's [start, end) range.

Usage: python build_intake_doc.py <DOCUMENT_ID>
"""
import json
import subprocess
import sys

BULLET = "bullet"
H1, H2, H3, BODY, MONO = "HEADING_1", "HEADING_2", "HEADING_3", "NORMAL_TEXT", "mono"

# (style, text) blocks. Each becomes one paragraph (text gets a trailing \n).
BLOCKS = [
    (H1, "CAE Promoter — contributor intake form"),
    (BODY, "This is the build spec for a new Google Form. Create the form with the "
           "questions below, in this order. The cae-promoter skill will generate a "
           "pre-filled link to this form (each field pre-populated from the "
           "contributor's session), which the contributor reviews and submits "
           "themselves — the skill never posts on their behalf."),

    (H2, "How to build it"),
    (BULLET, "Create a blank form at forms.new (or Drive → New → Google Forms)."),
    (BULLET, "Add each question below in order, using the field type noted in brackets."),
    (BULLET, "Mark the questions flagged Required as required."),
    (BULLET, "Leave settings at the defaults: do NOT require sign-in, do NOT limit to "
             "one response, do NOT collect email automatically. The pre-filled link "
             "depends on the form staying openly responder-accessible."),
    (BULLET, "When done, share the responder link (the /viewform URL) back with me so I "
             "can wire it into the skill."),

    (H2, "Questions"),

    (H3, "1. Full name  [Short answer] — Required"),
    (BODY, "Question text: What's your full name?"),
    (BODY, "Help text: As you'd like it credited in promotion (e.g., on the recording)."),

    (H3, "2. Job title  [Short answer] — Required"),
    (BODY, "Question text: What's your job title?"),
    (BODY, "Help text: Your current role (e.g., Senior Security Engineer)."),

    (H3, "3. Organization  [Short answer] — Required"),
    (BODY, "Question text: What organization do you work for?"),
    (BODY, "Help text: Company or team name."),

    (H3, "4. Work email  [Short answer, response validation: email] — Required"),
    (BODY, "Question text: What's the best email to reach you?"),
    (BODY, "Help text: We'll use this only to coordinate your promotion."),

    (H3, "5. GitHub handle  [Short answer] — Required"),
    (BODY, "Question text: What's your GitHub username?"),
    (BODY, "Help text: The account that owns (or submitted) the listing repo — e.g., octocat."),

    (H3, "6. Contributor type  [Multiple choice] — Required"),
    (BODY, "Question text: Which best describes you?"),
    (BULLET, "Tenable employee"),
    (BULLET, "Tenable partner"),
    (BULLET, "Community contributor"),

    (H3, "7. Team size  [Multiple choice] — Optional"),
    (BODY, "Question text: How big is your team?"),
    (BULLET, "Just me"),
    (BULLET, "2–10"),
    (BULLET, "11–50"),
    (BULLET, "51–200"),
    (BULLET, "200+"),

    (H3, "8. Organization size  [Multiple choice] — Optional"),
    (BODY, "Question text: How many people does your organization employ (or protect)?"),
    (BULLET, "1–50"),
    (BULLET, "51–500"),
    (BULLET, "501–5,000"),
    (BULLET, "5,001–25,000"),
    (BULLET, "25,000+"),

    (H3, "9. Industry  [Dropdown] — Optional"),
    (BODY, "Question text: What industry is your organization in?"),
    (BULLET, "Financial services and insurance"),
    (BULLET, "Healthcare and life sciences"),
    (BULLET, "Government and public sector"),
    (BULLET, "Technology and software"),
    (BULLET, "Retail and e-commerce"),
    (BULLET, "Manufacturing and industrial"),
    (BULLET, "Energy and utilities"),
    (BULLET, "Education"),
    (BULLET, "Telecommunications and media"),
    (BULLET, "Other"),

    (H3, "10. Region  [Dropdown] — Optional"),
    (BODY, "Question text: Where is your organization primarily based?"),
    (BULLET, "North America (US, Canada)"),
    (BULLET, "Latin America (Mexico, Central and South America, Caribbean)"),
    (BULLET, "Europe"),
    (BULLET, "Middle East and Africa"),
    (BULLET, "Asia-Pacific (incl. Australia and New Zealand)"),
    (BULLET, "Global / multiple regions"),
    (BULLET, "Other"),

    (H2, "Value statements"),
    (BODY, "These capture the quantifiable value statements the cae-promoter skill helped you "
           "shape — the firsthand results that lead your promotion (e.g., \"We cut our "
           "mean-time-to-respond by 88%\"). The skill will pre-fill these from your session; "
           "review each for accuracy before submitting. Enter one statement per field."),

    (H3, "11. Value statement 1  [Paragraph] — Required"),
    (BODY, "Question text: What's the primary value statement for your contribution?"),
    (BODY, "Help text: Lead with the strongest result. If it's an estimate rather than a "
           "measured figure, that's fine — just phrase it honestly."),

    (H3, "12. Value statement 2  [Paragraph] — Optional"),
    (BODY, "Question text: A second value statement, if you have one."),

    (H3, "13. Value statement 3  [Paragraph] — Optional"),
    (BODY, "Question text: A third value statement, if you have one."),

    (H3, "14. Future outreach  [Multiple choice] — Optional"),
    (BODY, "Question text: May we reach out about future projects and research?"),
    (BODY, "Help text: We'd love to feature your work again or invite you to contribute to "
           "future Tenable research. No obligation — say no and it won't affect this promotion."),
    (BULLET, "Yes, you can reach out"),
    (BULLET, "No, just this promotion"),

    (H2, "Getting the pre-fill field IDs (no API needed)"),
    (BODY, "After the form exists, I need each field's entry.<id> to build the pre-filled "
           "link. You can grab them without enabling any API:"),
    (BULLET, "In the form editor, open the ⋮ (top-right) menu → Get pre-filled link."),
    (BULLET, "Type a dummy answer into every field, then click Get link and copy it."),
    (BULLET, "Paste that whole URL back to me. It contains every entry.<id> mapped to the "
             "dummy values, which is all I need."),
    (BODY, "Share both the responder link and the pre-filled-sample link and I'll take it "
           "from there."),
]


def run(args, body=None):
    cmd = ["gws", "docs", "documents", args[0],
           "--params", json.dumps({"documentId": DOC_ID})]
    if body is not None:
        cmd += ["--json", json.dumps(body)]
    cmd += ["--format", "json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = "\n".join(l for l in res.stdout.splitlines() if "keyring backend" not in l)
    parsed = json.loads(out)
    return parsed


def clear_body():
    """Delete all existing body paragraphs so a rebuild starts from a blank doc."""
    doc = run(["get"])
    content = doc.get("body", {}).get("content", [])
    end = max((el.get("endIndex", 1) for el in content), default=1)
    # The final newline at end-1 cannot be deleted; delete [1, end-1).
    if end > 2:
        run(["batchUpdate"], {"requests": [
            {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1}}}
        ]})


def main():
    global DOC_ID
    DOC_ID = sys.argv[1]

    clear_body()

    # Build one insertText stream + record ranges. Insert sequentially at a
    # growing cursor starting at index 1.
    requests = []
    ranges = []  # (style, start, end)
    cursor = 1
    full_text = ""
    for style, text in BLOCKS:
        para = text + "\n"
        start = cursor
        end = cursor + len(para)
        ranges.append((style, start, end))
        full_text += para
        cursor = end

    # Single insert at index 1.
    requests.append({"insertText": {"location": {"index": 1}, "text": full_text}})

    # Apply named styles + bullets.
    for style, start, end in ranges:
        if style == BULLET:
            requests.append({"createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }})
        else:
            requests.append({"updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {"namedStyleType": style},
                "fields": "namedStyleType",
            }})

    res = run(["batchUpdate"], {"requests": requests})
    if "replies" in res or "documentId" in res:
        print(f"OK: applied {len(requests)} requests.")
    else:
        print("FAILED:", json.dumps(res)[:500])
        sys.exit(1)


if __name__ == "__main__":
    main()
