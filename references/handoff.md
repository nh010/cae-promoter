# Handoff — the courier procedure (session step 6)

The skill records/uploads nothing, holds no Tenable credentials, and opens the listing PR only on
the contributor's own auth. Declining leaves everything local, writes no manifest, and opens no PR.

## 1. Consent screen

Show the contributor **exactly what the bundle contains** and **any sensitive flags** from
`review_flags` (customer-named, third-party-cited, competitor-ui, brand-rule-trip). Nothing hands
off until they see this and explicitly approve.

## 2. Capture explicit approval

Only an explicit yes proceeds. On decline: stop here — everything stays local, no `handoff.yaml` is
written, no PR is opened.

## 3a. Riverside recording steps

Coach the contributor to record **both deliverables** (30–60s promo clip + 2–3 min demo) through the
team-owned shared async link, using `promo/video/recording-outline.md`:

`https://riverside.com/async-recording/invitation/78d41bff452767605718a1d666e5848d87ba7397`

Async gives a preview/re-record loop; coach "don't chase perfection — the team edits and finds the
best moments." Have them **paste back the Riverside preview/project link.** The skill does not
record, upload, edit, or host.

## 3b. Optional listing PR

If the contributor wants it, delegate the mechanics to `references/listing-pr.md` (cae-promoter's
own standalone `gh`/git flow on their auth). Capture the returned **PR URL**.

## 4. Write the manifest

Write `promo/handoff.yaml` from the template: the Riverside link + the promotion-edit PR URL (if
opened) + the asset identity, contributor type, socials (if opted in), capabilities run, and review
flags. Then print the exact next step: **"share this Riverside link with the Tenable AI Accelerator
Practice team."** In v1 the manifest is a local file the contributor relays by hand.
