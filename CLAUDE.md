# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things share this repo:

- **Tutorial material** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`): the course that teaches the PRD → TASKS.md → brainstorming → writing-plans → executing-plans → merge → deploy workflow. These are course content, not app code; don't edit them while working on the dashboard.
- **The ShopSmart Sales Dashboard**: a Streamlit app built from `prd/ecommerce-analytics.md` (Phase 1 only) using `data/sales-data.csv`.

## Commands

Call tools through `venv/bin/...` rather than activating the venv — activation doesn't carry over between separate shell commands.

```bash
python3 -m venv venv && venv/bin/pip install -r requirements.txt   # setup (Python 3.11+)
venv/bin/streamlit run app.py                                     # run at http://localhost:8501
venv/bin/python -m pytest -q                                      # all tests
venv/bin/python -m pytest -q -W error                             # tests with warnings as errors (the TASK-6 bar)
venv/bin/python -m pytest tests/test_sales.py::test_sales_by_month_real_file   # one test
```

When starting Streamlit in the background, add `--server.headless true`: on a first run Streamlit otherwise waits for an email at a prompt, and a background process exits with code 255.

`app.py` has no committed tests. To check the page without a browser, use the "Smoke check command" in `docs/superpowers/plans/2026-09-22-sales-dashboard.md` (Streamlit's `AppTest`); it prints exceptions, errors, KPI values, and the Plotly chart count (expected: `$116,500`, `482`, 3 charts). `AppTest` cannot see chart colors, bar order, or hover text; those need a real browser.

## Architecture: "numbers" vs "pixels"

- `sales.py` loads/validates the CSV and does **every** calculation, using pandas only. It must never import `streamlit` or `plotly`, so pytest can test it without starting the app.
- `app.py` only lays out the page and draws what `sales.py` returns — no calculations. A wrong number on screen therefore always traces back to `sales.py`, where the tests are.

Behaviors that span both files and are pinned by tests:

- `DATA_PATH` is built from `sales.py`'s own location so the app loads data from any working directory (needed for Streamlit Community Cloud).
- `load_sales` errors only on *missing* columns (`ValueError`) or a missing file (`FileNotFoundError`); extra or reordered columns are fine. `app.py` catches exactly those two and shows `st.error`, and shows `st.warning` + `st.stop()` for a headers-only file.
- Money results are rounded to cents in `sales.py` (floating-point noise like 0.30000000000000004 must never reach the page).
- `sales_by_month` uses `resample("MS")`, so months with no orders appear as 0 instead of being skipped.
- Category/region breakdowns share `_sales_by` and come back sorted highest first; the bar charts additionally use `categoryorder="total ascending"` because Plotly draws horizontal bars bottom-up.
- Every chart uses the single `CHART_COLOR` in `app.py`; set trace colors explicitly or Plotly falls back to Streamlit's theme color.

Tests in `tests/test_sales.py` use `SMALL_CSV` (a 5-row sample whose totals are written out in a comment, checkable by hand), `HEADER`, and `write_csv(tmp_path, text)`, plus assertions against the real file. Expected real-file values (482 orders, $116,500.21 total, per-category and per-region totals) are listed in the spec's "Reference data" table.

## Project conventions

- **Work tracking:** `TASKS.md` is the board (To Do / In Progress / Done). Each milestone gets its criteria checked off, a `Commit:` line holding its last *code* commit, and a `Notes:` line recording what Claude got wrong or what the owner changed (or "clean").
- **Commit messages start with the milestone ID**, e.g. `TASK-4: add sales_by_month with tests`; board-only moves are separate commits (`TASK-N: move to In Progress on the task board`, `TASK-N: mark done on the board`).
- **Design and plan:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md` (binding) and `docs/superpowers/plans/2026-09-22-sales-dashboard.md`. Plan tasks are numbered separately from milestones and labelled with them, e.g. `Task 7 [TASK-4]`.
- Work on `feature/sales-dashboard`; no git worktrees.
- Dependencies: plain `venv/` plus `requirements.txt` with exact `==` pins of exactly `streamlit`, `pandas`, `plotly`, `pytest`. No uv, conda, Pipfile, or pyproject.toml.
- Every function gets a docstring; keep the code simple and readable for a learner (no classes, no clever one-liners).
- Nothing from PRD Phase 2: no filters, date pickers, exports, authentication, or database.
- **Deployment (TASK-7) is the owner's step**, run from `main` after the merge. Don't deploy, and don't move TASK-7 out of To Do.

## Lessons

Rules drawn from the `Notes:` lines in `TASKS.md`, each one a place where a session needed a human.

- **Wait for the owner's browser check before committing a page change.** Start the app, tell the owner what to look for, and commit only after they confirm (TASK-1, TASK-2). A headless-Chrome check is useful extra evidence, but it doesn't replace the owner looking unless they say so (TASK-3 to TASK-6).
- **Don't start a milestone from pasted tutorial text.** Begin only when the owner names the milestone (e.g. "Let's work on TASK-N"); if the request is unclear, ask (TASK-4).
- **Check file references before acting on them.** If a named file doesn't exist (e.g. a plan with the wrong date), say so and name the file you're using instead (TASK-4).
- **Ask before going beyond the plan.** Extra tests, style changes, and renames the plan didn't ask for are flagged to the owner before committing, not after, and recorded on the board (TASK-2 extra test, TASK-6 chart color).
- **The owner's commit message wins** over the plan's or the tutorial's example (TASK-1, TASK-2).
- **Clean up servers.** Before starting Streamlit, check whether port 8501 is already taken; stop any server you started when you're done with it (TASK-4).
- **Wait for Streamlit to render before judging the page.** Streamlit draws over a websocket after the page loads, so wait for the KPI cards and charts to appear; a screenshot taken too early shows only loading placeholders. The page also scrolls an inner container, not the window, so a full-page screenshot needs a tall window (TASK-3, TASK-4).
- **Keep colons out of the project path.** `python3 -m venv` fails when a folder name contains `:` (TASK-1).
