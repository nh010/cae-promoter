# Listing PR — cae-promoter's own standalone fork→PR flow (capability C)

This is cae-promoter's **own** implementation of the fork→PR sequence — explicitly **not** a
dependency on, import of, or call into the `cyberagents-exchange-submit` skill (that skill is a
conceptual sibling only; the two ship and version independently). Runs only on the **contributor's
own GitHub auth**, holds no Tenable credential, and is gated on **explicit approval** — it opens
nothing on decline.

## When to offer it

During capability C (on-Exchange optimization), once the promo section, woven-in value statements,
and any verified `works_with_hexa` badge are ready to land on the listing. Offer; don't assume.

## The `gh`/git sequence (contributor's auth)

1. `gh auth status` — if unauthenticated, **bail with a clear message** ("run `gh auth login`
   first, then re-run") and open nothing.
2. Fork `tenable/cyberagents-exchange` (or reuse an existing fork).
3. Create a branch (e.g. `promote-<slug>`).
4. Edit the listing file `<type>/<slug>.md` — add the promo section + value statements, set
   `works_with_hexa`/badge **only where the repo confirmed it** — and any README changes.
5. Commit → push to the fork.
6. `gh pr create` with a generated title/body → capture the returned **PR URL** (record it in the
   promo record's `promotion_edit_pr.url` and, on handoff, `handoff.yaml`).

## Claude-native fallback (deferred Desktop variant)

When `gh`/Python isn't available (the Desktop variant), print the exact manual `gh`/git steps for
the contributor to run themselves — the same workaround submitter-skill users without Claude Code
already use. The skill walks them through it; it still opens nothing on their behalf.

## Boundary

This is the contributor's action on the contributor's listing and credentials. It is **not** acting
as Tenable. Distinguish it from any request to post as Tenable or push into a Tenable-owned
channel — those are refused (see `guardrail-gates.md`).
