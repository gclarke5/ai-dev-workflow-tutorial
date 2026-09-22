# ShopSmart Sales Dashboard — Design

**Date:** 2026-09-22
**Source requirements:** `prd/ecommerce-analytics.md` (Phase 1 only)
**Milestones:** `TASKS.md` (TASK-1 to TASK-7)
**Branch:** `feature/sales-dashboard`

## 1. Goal

Build the Phase 1 sales dashboard described in the PRD: two KPI cards, a monthly sales trend line chart, and bar charts for sales by category and by region, all read from `data/sales-data.csv`. The dashboard is done when every item in the PRD's acceptance checklist passes and every number on screen matches the CSV exactly.

Nothing from Phase 2 is built: no filters, date pickers, exports, authentication, or database.

## 2. Constraints

- Work directly on `feature/sales-dashboard`, with no git worktree.
- Use a plain Python virtual environment in `venv/`. List dependencies in `requirements.txt` with exact version pins. No uv, conda, Pipfile, or pyproject.toml.
- Keep the data calculations in their own module, covered by pytest tests.
- Keep the code simple and readable for someone learning.
- The owner deploys to Streamlit Community Cloud from `main` after the merge. Implementation stops before deployment.

## 3. Reference data

These values were measured directly from `data/sales-data.csv`. The tests use them as expected results.

| Fact | Value |
|---|---|
| Rows | 482 (one per unique `order_id`) |
| Date range | 2024-01-03 to 2024-12-31 |
| Total sales | 116,500.21 |
| `quantity × unit_price == total_amount` | true on every row |

| Category | Sales |
|---|---|
| Electronics | 42,683.67 |
| Wearables | 23,698.23 |
| Audio | 19,638.44 |
| Smart Home | 19,317.23 |
| Accessories | 11,162.64 |

| Region | Sales |
|---|---|
| North | 38,857.24 |
| West | 27,463.74 |
| East | 26,783.53 |
| South | 23,395.70 |

## 4. Architecture

There are two modules, split into "numbers" and "pixels":

```
app.py              # Streamlit page: title, KPI cards, 3 charts (no calculations)
sales.py            # pandas only: load/validate the CSV + all calculations
tests/test_sales.py # pytest tests for sales.py
requirements.txt    # exact pins: streamlit, pandas, plotly, pytest
data/sales-data.csv # existing data file
```

`sales.py` never imports Streamlit or Plotly, so pytest can test it without starting the app. `app.py` only displays values it gets from `sales.py`, so a wrong number on screen can only come from `sales.py`, and the tests there would catch it.

**Data flow:** `load_sales("data/sales-data.csv")` → the calculation functions in `sales.py` → Streamlit and Plotly in `app.py`.

## 5. Data module: `sales.py`

| Function | Returns | Behavior |
|---|---|---|
| `load_sales(path)` | DataFrame | Reads the CSV and parses `date` as dates. Raises `ValueError` naming every missing column when any of the 8 expected columns (`date, order_id, product, category, region, quantity, unit_price, total_amount`) is absent. Raises `FileNotFoundError` with the path when the file does not exist. |
| `total_sales(df)` | float | Sum of `total_amount`. |
| `total_orders(df)` | int | Number of unique `order_id` values. |
| `sales_by_month(df)` | DataFrame with `month`, `sales` | Sum of `total_amount` per calendar month, in chronological order. `month` is the first day of each month as a date. |
| `sales_by_category(df)` | DataFrame with `category`, `sales` | Sum per category, sorted highest first. |
| `sales_by_region(df)` | DataFrame with `region`, `sales` | Sum per region, sorted highest first. |

`sales_by_category` and `sales_by_region` both call one private helper, `_sales_by(df, column)`, so the group-and-sort logic is written once.

## 6. Page: `app.py`

- **Page config:** `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")`.
- **Loading:** a small wrapper around `load_sales`, decorated with `@st.cache_data`, so the CSV is read once rather than on every rerun.
- **Error handling:** if loading raises `ValueError` or `FileNotFoundError`, the page shows `st.error(<message>)` and calls `st.stop()`. The viewer sees one plain sentence instead of a traceback.

Layout, top to bottom:

1. **Title:** "ShopSmart Sales Dashboard", with a caption giving the data's date range (derived from the data, not hard-coded).
2. **KPI row:** two `st.metric` cards in two columns.
   - Total Sales in whole dollars with thousands separators: `$116,500`.
   - Total Orders with thousands separators: `482`.
3. **Sales trend:** a full-width Plotly line chart of `sales_by_month`, with points shown on the line.
   - X-axis "Month", labelled Jan–Dec.
   - Y-axis "Sales ($)".
   - Hover shows the month and the exact amount, e.g. `$10,234.56`.
4. **Breakdowns:** two columns, each holding a horizontal Plotly bar chart.
   - Left: "Sales by Category". Right: "Sales by Region".
   - The biggest bar is on top: the y-axis uses `categoryorder="total ascending"`, because Plotly draws horizontal bars from the bottom up.
   - Hover shows the exact dollar amount.

**Styling:** Plotly's default template, one consistent bar color, and clear titles and axis labels on every chart. No custom CSS.

## 7. Testing

The functions in `sales.py` are developed test-first: each test is written and seen failing before its implementation. Most tests use a small hand-made CSV of about 5 rows, written to pytest's `tmp_path`, so expected values can be worked out by hand. A few tests run against the real `data/sales-data.csv` and assert the reference values from Section 3.

| Test | Asserts |
|---|---|
| load real file | 482 rows; `date` has a datetime dtype |
| missing column | `ValueError` whose message names the missing column |
| missing file | `FileNotFoundError` |
| total sales | exact sum on the small CSV; `116500.21` on the real file (compared with `pytest.approx`) |
| total orders | a duplicated `order_id` counts once; `482` on the real file |
| by month | chronological order; the monthly sales add up to the total; 12 rows on the real file |
| by category | sorted highest first; Electronics first on the real file |
| by region | sorted highest first; North first on the real file |

`app.py` has no automated tests. It is checked in each milestone by running `streamlit run app.py` and looking at the page, per the Definition of Done in `TASKS.md`.

## 8. Milestone mapping

| Milestone | Scope |
|---|---|
| TASK-1 | Create `venv/`; install and pin `requirements.txt`; stub `app.py` with the page config and title |
| TASK-2 | `load_sales` with validation (test-first); page section layout in `app.py` |
| TASK-3 | `total_sales`, `total_orders` (test-first); KPI cards |
| TASK-4 | `sales_by_month` (test-first); trend line chart |
| TASK-5 | `sales_by_category`, `sales_by_region` (test-first); two bar charts |
| TASK-6 | Check every PRD acceptance criterion; confirm no errors or warnings; confirm the page loads in under 5 seconds; final polish |
| TASK-7 | **Owner executes:** merge to `main`, then deploy to Streamlit Community Cloud. Implementation stops here and hands off. |

The implementation plan numbers its own tasks 1, 2, 3… and tags each one with its milestone (e.g. **[TASK-3]**). Commit messages start with the milestone ID (e.g. `TASK-3: add total_sales with tests`).

## 9. Out of scope

- All PRD Phase 2 items
- Tests for `app.py` rendering
- Row-level data validation (bad dates, negative amounts)
- Custom theming or CSS
