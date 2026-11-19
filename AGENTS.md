# AGENTS.md — myproject

<!-- One paragraph: what the project is, for whom, and the stack. Example:
     "An autonomous X for one Y. Python 3.14, Pydantic v2, <main external API>." -->

## Read first — your slice, not whole files

1. Your task: `make prompt S=<id>` prints the common header and your session's prompt
   (`docs/sessions/<id>-<slug>.md`).
2. `docs/MASTER_PLAN.md` — the design. Do not re-derive or relitigate it. Read the §§ your
   prompt names, in full, before writing code; other §§ when a question sends you there.
3. `docs/decisions/` — one file per decision: why things are as they are and what was
   rejected. Read `docs/decisions/README.md` (the index), then the entries that cite your §§
   or touch your modules, and the previous session's.
4. `docs/ROADMAP.md` — "What runs next", the latest session-log entry, and the Follow-ups and
   Live verification queue entries that name your session (search, do not read them whole).
5. `docs/knowledge/` — observed behaviour of external services, tagged by route and date:
   the files your work touches.

Find sections with `grep -n '^#'` and read them by line range. If the code contradicts the
plan or your prompt, stop and report it in the PR description before writing code around it.

## Context budget

- Read what the work in front of you needs, when it needs it. Large data files (fixtures,
  CSVs) are inspected by script, `head` or `grep`, never read whole.
- Read at the source yourself what you port or edit, and every critical-path mechanic.
- Never poll. Background subagents and CI report when they finish.
- `docs/archive/` and finished sessions in `docs/sessions/done/` are searched, never read whole.

## Build for evidence

- Nothing is built "for later". A prompt's `DO NOT BUILD` list is part of its scope; if the
  work seems to need something on it, stop and report.
- A session ends with something observable: a verdict, a command the owner can run, or a
  behaviour a test shows.

## Hard rules (safety)

<!-- The project's non-negotiables, each one enforced in code or by a test, not only here.
     ObliskIQ's, as an example of the level of precision:
     - Money paths fail closed: unknown reply → cancel and alert.
     - Idempotency: the intent id is the client order id; look it up before any placement.
     - Kill switch must work when everything else is failing. -->

- Never print, log or commit secrets, account ids, tokens, `.env` files, keys or personal
  data. Prompts sent to LLMs carry no identifiers.
- Cloud sessions never hold production credentials. Without credentials, build against
  fixtures and mark checks `VERIFY-LIVE(<what>)` in code and in `docs/ROADMAP.md` →
  "Live verification queue".

## Engineering rules

- **Nothing hardcoded.** Values live in `config/` (expert defaults in `config/defaults/`,
  owner overrides in `config/owner.yaml`). Every key has a consumer; no magic numbers on a
  critical path.
- **One owner per fact.** Config = values; code = mechanics; `docs/decisions/` = why;
  `docs/knowledge/` = observed external behaviour; `MASTER_PLAN.md` = design.
- **Honest degradation.** Missing or immature input → explicit status. Never fabricate,
  silently interpolate or substitute an unlabelled proxy.
- Pydantic v2 only; domain models frozen with `extra="forbid"` (`myproject.domain.DomainModel`).
- Timezone-aware UTC datetimes; local time through `zoneinfo`. `Decimal` for money.
- asyncio for I/O; no blocking calls in the event loop; no mutable module globals.
- Search before creating. Extend existing code rather than writing parallel versions.
- `mypy --strict` on `src/`. Architecture boundaries are import-linter contracts in
  `pyproject.toml`; a new layer gets its contract in the same PR.
- Small commits with conventional prefixes (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`,
  `chore:`).
- Documents state the current truth. No version banners or change narratives inside docs or
  code comments — history belongs in git, `CHANGELOG.md` and `docs/decisions/`.

## Testing rules

- `make check` = `ruff format --check`, `ruff check`, `mypy --strict src`, `lint-imports`,
  `pytest` (parallel) with the coverage floor. Green before opening a PR and before merging.
- No network in tests: HTTP mocked with `respx`; fixtures in `tests/fixtures/` with a sidecar
  note of source and date. Live probes are separate commands, never tests.
- Critical paths need failure-branch tests, not only the happy path.
- The coverage floor in `pyproject.toml` is raised on purpose, never lowered to fit.

## CI budget (private repository on GitHub Free)

Every CI run is billed against a small monthly allowance.

- Run `make check` locally and push once it is green; batch fixes into one push, never one
  push per fix. Each push to an open PR is a full CI run.
- CI runs on pull requests only. Prose-only changes (`docs/`, `*.md`) skip it: run
  `make check` locally for those and say so in the PR.
- Never add a workflow, a matrix or a scheduled job without a decision in `docs/decisions/`
  that states its monthly cost in minutes.
- Dependabot pull requests belong to the maintenance session (`make prompt S=maintenance`),
  never to a build session.

## Session workflow

1. Read the files above. Branch `s<NN>-<short-slug>` from an up-to-date `main`.
2. Put your plan (5–15 bullets) at the top of the PR description. Do not wait for approval
   unless a stop condition applies.
3. Keep to your prompt's scope; anything else goes to "Follow-ups" in the PR and ROADMAP.
4. In the same PR: the session-log entry in `docs/ROADMAP.md` (at most 15 lines: landed,
   deferred, live findings, VERIFY-LIVE items); a new file in `docs/decisions/` per real
   decision (at most 12 lines, added to the index); a `CHANGELOG.md` section; the version in
   `pyproject.toml` (minor per session, patch for fixes). Move your prompt file to
   `docs/sessions/done/`. Never create or push tags: the release workflow does.
5. You may correct later prompts in `docs/sessions/` only to fix facts, paths or
   dependencies your work changed — never to add scope. Log each edit.
6. If you cannot finish everything with quality, merge a coherent, tested subset and add
   `docs/sessions/<id>a-<slug>.md` with the remainder.

## End-of-session protocol (mandatory, performed by the agent)

Where `gh` is missing or unauthenticated, the environment's GitHub tools do the same steps.

1. **PR.** Push and open it with `gh pr create` using `.github/pull_request_template.md`.
2. **Self-review.** Wait for CI (`gh pr checks <n> --watch`) and review the PR against the
   prompt: every changed critical-path file in full (`git diff origin/main...HEAD -- <path>`),
   the rest from `git diff --stat`. Check for bugs; stubbed or lazily implemented modules;
   safety-rule violations; hardcoded values; missing failure-branch tests; dead code, debug
   prints, stray files, TODOs without an issue, secrets; docs consistency. Tick the checklist.
3. **Fix.** Found issues or red CI → fix all of them, run `make check` locally, push once. At
   most three fix rounds.
4. **Merge.** Only with green CI and all issues resolved: `gh pr merge <n> --squash`; if the
   proxy refuses, `gh api -X PUT repos/{owner}/{repo}/pulls/<n>/merge -f merge_method=squash`.
   Then `git checkout main && git pull` and run `make check` on `main`; if it is red, open a
   fix PR at once under this protocol.
5. **Release.** If the version changed, confirm the release run succeeded
   (`gh run list --workflow release.yml --limit 1`) and `gh release view v<version>` exists.

Never merge with failing CI, unresolved blocking findings, or an unchecked safety box. After
three rounds with blockers left: leave the PR open, label it `needs-owner`, and summarise why.

## Stop conditions (stop, report in the PR, do not improvise)

- The plan or prompt contradicts the code or a recorded decision.
- A step needs live credentials, an account action, a paid service or an irreversible change.
- A test can only pass by weakening a safety rule.
- An external behaviour is unknown and guessing would affect a critical path.

## Commands

```
make setup                 # uv sync, pre-commit hooks
make check                 # format, lint, types, import contracts, tests, coverage
make test                  # pytest only
make prompt S=01           # the prompt for session 01
uv run myproject --help
```

## Layout

`src/myproject/` per `docs/MASTER_PLAN.md` → Layout · `config/` · `tests/` · `docs/` ·
`scripts/`.
