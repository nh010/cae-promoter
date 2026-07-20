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

## 3a. Recording — set expectations, don't hand a link

The skill has **no** recording link to give. Tell the contributor plainly: **once they submit the
intake form (Step 5), Tenable emails them a virtual recording studio link.** The skill's job here is
to make sure they're ready — walk them through `promo/video/recording-outline.md` so the promo-clip
script and demo outline are set before the link arrives.

Coach the recording itself: they'll record **both deliverables** (30–60s promo clip + 2–3 min demo)
at the studio; the async studio gives a preview/re-record loop; "don't chase perfection — the team
edits and finds the best moments." The skill does not record, upload, edit, or host.

## 3b. Optional listing PR

If the contributor wants it, delegate the mechanics to `references/listing-pr.md` (cae-promoter's
own standalone `gh`/git flow on their auth). Capture the returned **PR URL**.

## 4. Write the manifest

Write `promo/handoff.yaml` from the template: the promotion-edit PR URL (if opened) + the asset
identity, contributor type, socials (if opted in), capabilities run, and review flags. The recording
link is **not** captured here — it's emailed to the contributor by Tenable after form submission and
lives in their inbox, not the manifest. Then print the exact next step: **"submit the intake form,
then watch your inbox for the recording studio link from Tenable."** In v1 the manifest is a local
file the contributor relays by hand.
