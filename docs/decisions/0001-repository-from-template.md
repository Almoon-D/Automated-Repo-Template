# 0001 — Repository conventions from the template

- Date: 2026-11-18 · Status: accepted
- Context: a private repository on GitHub Free, built by agent sessions that open, review
  and merge their own pull requests.
- Decision: CI on pull requests only, skipped for prose; Dependabot monthly, grouped, with
  cooldown and no automatic rebases, merged by the monthly maintenance session; releases
  published from `CHANGELOG.md` when the version changes; one file per decision and per
  session prompt so an agent reads only its slice.
- Rejected: CI on every push to `main` (it repeats the pull request's run); weekly
  Dependabot with automatic rebases (each rebase is a full CI run).
- Cost: about one CI run per pull request plus one per Dependabot batch.
