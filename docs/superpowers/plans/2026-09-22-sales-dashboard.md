# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 ShopSmart sales dashboard (two KPI cards, a monthly trend line, and bar charts for category and region) as a Streamlit app that reads `data/sales-data.csv`.

**Architecture:** `sales.py` holds every calculation as a plain pandas function and is covered by pytest tests written first. `app.py` only lays out the page: it calls `sales.py` and draws the results with Streamlit and Plotly. The CSV is read once through `@st.cache_data`.

**Tech Stack:** Python 3.11+ (local: 3.14), Streamlit, pandas, Plotly Express, pytest. Plain `venv/` + `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

## How this plan is numbered

- **Plan tasks** are numbered **Task 1 … Task 11**. That is the build order.
- **Milestones** come from `TASKS.md` and are written **TASK-1 … TASK-7**. Every plan task names its milestone in its heading, e.g. `Task 4 [TASK-3]`.
- Every commit message starts with the milestone ID, e.g. `TASK-3: add total_sales and total_orders with tests`.

| Milestone | Plan tasks |
|---|---|
| TASK-1 Environment setup | Task 1 |
| TASK-2 Data loading and basic structure | Task 2, Task 3 |
| TASK-3 KPI cards | Task 4, Task 5 |
| TASK-4 Sales trend chart | Task 6, Task 7 |
| TASK-5 Category and region breakdowns | Task 8, Task 9 |
| TASK-6 Testing and refinement | Task 10 |
| TASK-7 Deployment | Task 11 (**owner executes**; the plan stops here) |

## Global Constraints

- Work on the existing branch `feature/sales-dashboard`. Do not create a git worktree or any other branch.
- Dependencies live in a plain virtual environment at `venv/` (already in `.gitignore`). Do not use uv, conda, Pipfile, or pyproject.toml.
- `requirements.txt` pins exact versions (`name==X.Y.Z`) of exactly four packages: `streamlit`, `pandas`, `plotly`, `pytest`.
- All calculations live in `sales.py`, which must not import `streamlit` or `plotly`. `app.py` contains no calculations.
- Every function in `sales.py` gets a docstring. Keep the code simple and readable for a learner: no classes, no clever one-liners.
- Nothing from PRD Phase 2: no filters, date pickers, exports, authentication, or database.
- Do **not** edit `TASKS.md`. The owner moves milestones and fills in the Commit lines.
- Do **not** push, merge, or deploy. Commit locally only.
- Run every command from the project root. Call tools through `venv/bin/...` (e.g. `venv/bin/python -m pytest`) instead of activating the venv, because activation doesn't carry over between separate shell commands.

## Review Focus

Five situations the spec implies but doesn't spell out. Each one is pinned by a test in the task noted:

1. **Starting the app from another folder.** Streamlit Community Cloud, or `streamlit run path/to/app.py`, may start from a different working directory, and the data must still load. `DATA_PATH` is built from `sales.py`'s own location. Tested in Task 2 (`test_data_path_is_absolute_and_exists`).
2. **A CSV with an extra column or columns in a different order.** It should still load, because only *missing* columns are an error. Tested in Task 2 (`test_load_sales_allows_extra_columns_in_any_order`).
3. **Floating-point noise in money sums.** Adding up cents like 0.10 + 0.20 must show as 0.30, not 0.30000000000000004. Totals and breakdowns are rounded to cents. Tested in Task 4 (`test_total_sales_is_rounded_to_cents`) and Task 8 (`test_breakdowns_are_rounded_to_cents`).
4. **A CSV with headers but no rows.** The KPIs should be 0 and nothing should crash. The page shows a warning and stops. Tested in Task 4 (`test_totals_on_headers_only_file_are_zero`), and handled in `app.py` from Task 3.
5. **A month with no sales.** The trend should show that month as $0, not skip it and draw a misleading line. Tested in Task 6 (`test_sales_by_month_fills_missing_months_with_zero`).

## Reference values (measured from `data/sales-data.csv`)

| Fact | Value |
|---|---|
| Rows / unique order IDs | 482 / 482 |
| Date range | 2024-01-03 to 2024-12-31 |
| Total sales | 116500.21 |
| Category sales | Electronics 42683.67, Wearables 23698.23, Audio 19638.44, Smart Home 19317.23, Accessories 11162.64 |
| Region sales | North 38857.24, West 27463.74, East 26783.53, South 23395.70 |

## Smoke check command (used by the page tasks)

This runs `app.py` headlessly with Streamlit's built-in `AppTest` and prints what the page shows. It is a verification command, **not** a committed test file.

```bash
venv/bin/python - <<'EOF'
import time
from pathlib import Path
from streamlit.testing.v1 import AppTest

start = time.perf_counter()
at = AppTest.from_file(str(Path("app.py").resolve())).run(timeout=30)
print(f"run time: {time.perf_counter() - start:.2f}s")
print("exceptions:", [e.value for e in at.exception])
print("errors:", [e.value for e in at.error])
print("title:", [t.value for t in at.title])
print("subheaders:", [s.value for s in at.subheader])
print("metrics:", [(m.label, m.value) for m in at.metric])
print("plotly charts:", len(at.get("plotly_chart")))
EOF
```

## File Structure

| File | Responsibility | Created in |
|---|---|---|
| `requirements.txt` | Exact pins for streamlit, pandas, plotly, pytest | Task 1 |
| `pytest.ini` | Tells pytest where the tests are and lets them `import sales` from the project root | Task 1 |
| `app.py` | Streamlit page: layout, KPI cards, charts, error message. No calculations. | Task 1, grown in Tasks 3, 5, 7, 9 |
| `sales.py` | Load and validate the CSV; every calculation | Task 2, grown in Tasks 4, 6, 8 |
| `tests/test_sales.py` | pytest tests for `sales.py` | Task 2, grown in Tasks 4, 6, 8 |

---

### Task 1 [TASK-1]: Virtual environment, pinned requirements, app stub

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `app.py`

**Interfaces:**
- Consumes: nothing
- Produces: `venv/` with the four packages installed; `app.py` that sets the page config and shows the title "ShopSmart Sales Dashboard"

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`
Then: `venv/bin/python --version`
Expected: `Python 3.11` or higher (this machine has 3.14.x).

- [ ] **Step 2: Install the four packages**

Run: `venv/bin/python -m pip install --upgrade pip && venv/bin/python -m pip install streamlit pandas plotly pytest`
Expected: ends with `Successfully installed ...` and no errors. If any package fails to install on this Python version, stop and report the error to the owner rather than switching tools.

- [ ] **Step 3: Write `requirements.txt` with the exact installed versions**

Run: `venv/bin/python -m pip freeze | grep -i -E '^(streamlit|pandas|plotly|pytest)==' > requirements.txt && cat requirements.txt`
Expected: exactly four lines, in the form `pandas==X.Y.Z`, `plotly==X.Y.Z`, `pytest==X.Y.Z`, `streamlit==X.Y.Z`. Only the top-level packages are pinned; pip resolves their dependencies.

- [ ] **Step 4: Confirm `requirements.txt` installs cleanly**

Run: `venv/bin/python -m pip install -r requirements.txt`
Expected: every line says `Requirement already satisfied`.

- [ ] **Step 5: Create `pytest.ini`**

```ini
[pytest]
testpaths = tests
pythonpath = .
```

- [ ] **Step 6: Create the stub `app.py`**

```python
"""ShopSmart Sales Dashboard.

Run locally with:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 7: Smoke-check the page**

Run the smoke check command from the top of this plan.
Expected: `exceptions: []`, `errors: []`, `title: ['ShopSmart Sales Dashboard']`.

- [ ] **Step 8: Owner check in the browser**

Start the app in the background: `venv/bin/streamlit run app.py --server.headless true`
Tell the owner to open http://localhost:8501 and confirm the page shows the title "ShopSmart Sales Dashboard". Wait for their confirmation, then stop the server.

- [ ] **Step 9: Confirm `venv/` is ignored, then commit**

Run: `git status --short`
Expected: `app.py`, `pytest.ini`, `requirements.txt` are listed, and `venv/` is **not**.

```bash
git add app.py pytest.ini requirements.txt
git commit -m "TASK-1: set up venv, pinned requirements, and app stub"
```

---

### Task 2 [TASK-2]: `load_sales` with column validation

**Files:**
- Create: `sales.py`
- Test: `tests/test_sales.py`

**Interfaces:**
- Consumes: nothing
- Produces, in `sales.py`:
  - `EXPECTED_COLUMNS: list[str]`, the 8 required column names
  - `DATA_PATH: pathlib.Path`, the absolute path to `data/sales-data.csv`
  - `load_sales(path=DATA_PATH) -> pandas.DataFrame`, with `date` as `datetime64`. Raises `FileNotFoundError` if the file is missing, and `ValueError` naming every missing column.
- Produces, in `tests/test_sales.py`: `SMALL_CSV` (a 5-row sample) and `write_csv(tmp_path, text) -> Path`, which later tasks reuse.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sales.py`:

```python
"""Tests for sales.py, the dashboard's data module."""
import pandas as pd
import pytest

import sales

# A tiny sample small enough to check by hand.
# Totals: all = 1300.00; Jan = 520.00, Feb = 80.00, Mar = 700.00
# Category: Electronics 1000, Wearables 200, Audio 80, Accessories 20
# Region: North 580, West 500, East 200, South 20
SMALL_CSV = """date,order_id,product,category,region,quantity,unit_price,total_amount
2024-01-05,ORD-1,Laptop,Electronics,North,1,500.00,500.00
2024-01-20,ORD-2,Phone Case,Accessories,South,2,10.00,20.00
2024-02-10,ORD-3,Earbuds,Audio,North,1,80.00,80.00
2024-03-15,ORD-4,Smart Watch,Wearables,East,1,200.00,200.00
2024-03-28,ORD-5,Laptop,Electronics,West,1,500.00,500.00
"""

HEADER = "date,order_id,product,category,region,quantity,unit_price,total_amount\n"


def write_csv(tmp_path, text):
    """Write text to a CSV file in pytest's temporary folder and return its path."""
    path = tmp_path / "sales.csv"
    path.write_text(text)
    return path


# --- load_sales -------------------------------------------------------------

def test_load_sales_reads_real_file():
    df = sales.load_sales()
    assert len(df) == 482
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_reads_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    assert len(df) == 5
    assert df["date"].min() == pd.Timestamp("2024-01-05")


def test_load_sales_names_missing_column(tmp_path):
    no_region = (
        "date,order_id,product,category,quantity,unit_price,total_amount\n"
        "2024-01-05,ORD-1,Laptop,Electronics,1,500.00,500.00\n"
    )
    with pytest.raises(ValueError, match="region"):
        sales.load_sales(write_csv(tmp_path, no_region))


def test_load_sales_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        sales.load_sales(tmp_path / "does-not-exist.csv")


def test_load_sales_allows_extra_columns_in_any_order(tmp_path):
    reordered = (
        "total_amount,region,notes,date,order_id,product,category,quantity,unit_price\n"
        "500.00,North,gift,2024-01-05,ORD-1,Laptop,Electronics,1,500.00\n"
    )
    df = sales.load_sales(write_csv(tmp_path, reordered))
    assert len(df) == 1


def test_data_path_is_absolute_and_exists():
    assert sales.DATA_PATH.is_absolute()
    assert sales.DATA_PATH.exists()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `venv/bin/python -m pytest -v`
Expected: collection error, `ModuleNotFoundError: No module named 'sales'`.

- [ ] **Step 3: Write `sales.py`**

```python
"""Data loading and calculations for the ShopSmart sales dashboard.

Every number the dashboard shows is calculated here, so it can be tested
with pytest without starting Streamlit. This module never imports streamlit.
"""
from pathlib import Path

import pandas as pd

# Built from this file's location so the app works from any working folder.
DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

EXPECTED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]


def load_sales(path=DATA_PATH):
    """Read the sales CSV and return it as a DataFrame with real dates.

    Raises FileNotFoundError if the file does not exist, and ValueError
    listing any expected columns that are missing.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Sales data file not found: {path}")

    df = pd.read_csv(path)

    missing = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"{path.name} is missing column(s): {', '.join(missing)}")

    df["date"] = pd.to_datetime(df["date"])
    return df
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `venv/bin/python -m pytest -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add sales.py tests/test_sales.py
git commit -m "TASK-2: add load_sales with column validation and tests"
```

---

### Task 3 [TASK-2]: Load data in the page and lay out its sections

**Files:**
- Modify: `app.py` (replace the whole file)

**Interfaces:**
- Consumes: `sales.load_sales(path)`, `sales.DATA_PATH` (Task 2)
- Produces: in `app.py`, `get_sales_data()`, which returns the cached DataFrame; the variable `df` for the rest of the page; the subheaders "Sales Trend Over Time", "Sales by Category", "Sales by Region"; and the two column containers `left` and `right`

- [ ] **Step 1: Replace `app.py`**

```python
"""ShopSmart Sales Dashboard.

Shows total sales, total orders, the monthly sales trend, and sales by
category and region, all calculated in sales.py from data/sales-data.csv.

Run locally with:  streamlit run app.py
"""
import streamlit as st

import sales

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales_data():
    """Load the sales CSV once and reuse it every time the page reruns."""
    return sales.load_sales(sales.DATA_PATH)


st.title("ShopSmart Sales Dashboard")

# Show a plain message instead of a traceback if the data can't be loaded.
try:
    df = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

if df.empty:
    st.warning("The sales data file has no rows to show.")
    st.stop()

st.caption(f"Sales from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")

# --- Sales trend ---
st.subheader("Sales Trend Over Time")

# --- Breakdowns ---
left, right = st.columns(2)
with left:
    st.subheader("Sales by Category")
with right:
    st.subheader("Sales by Region")
```

- [ ] **Step 2: Smoke-check the page**

Run the smoke check command from the top of this plan.
Expected: `exceptions: []`, `errors: []`, `title: ['ShopSmart Sales Dashboard']`, `subheaders: ['Sales Trend Over Time', 'Sales by Category', 'Sales by Region']`.

- [ ] **Step 3: Run the tests (unchanged, should still pass)**

Run: `venv/bin/python -m pytest -v`
Expected: 6 passed.

- [ ] **Step 4: Owner check in the browser**

Start the app in the background: `venv/bin/streamlit run app.py --server.headless true`
Tell the owner to open http://localhost:8501 and confirm they see the title, the caption "Sales from January 2024 to December 2024", and the three section headings, with "Sales by Category" and "Sales by Region" side by side. Wait for their confirmation, then stop the server.

- [ ] **Step 5: Commit**

```bash
git add app.py
git commit -m "TASK-2: load sales data in the page and lay out its sections"
```

---

### Task 4 [TASK-3]: `total_sales` and `total_orders`

**Files:**
- Modify: `sales.py` (append two functions)
- Test: `tests/test_sales.py` (append tests)

**Interfaces:**
- Consumes: `sales.load_sales`, and in the tests `SMALL_CSV`, `HEADER`, `write_csv` (Task 2)
- Produces: `sales.total_sales(df) -> float` (rounded to cents), `sales.total_orders(df) -> int` (unique `order_id` count)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales.py`:

```python
# --- total_sales / total_orders ---------------------------------------------

def test_total_sales_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    assert sales.total_sales(df) == 1300.00


def test_total_sales_real_file():
    df = sales.load_sales()
    assert sales.total_sales(df) == pytest.approx(116500.21)


def test_total_sales_is_rounded_to_cents(tmp_path):
    text = HEADER + (
        "2024-01-01,ORD-1,Cable,Accessories,North,1,0.10,0.10\n"
        "2024-01-02,ORD-2,Cable,Accessories,North,1,0.20,0.20\n"
    )
    df = sales.load_sales(write_csv(tmp_path, text))
    assert sales.total_sales(df) == 0.30


def test_total_orders_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    assert sales.total_orders(df) == 5


def test_total_orders_counts_each_order_id_once(tmp_path):
    text = HEADER + (
        "2024-01-01,ORD-1,Laptop,Electronics,North,1,500.00,500.00\n"
        "2024-01-01,ORD-1,Phone Case,Accessories,North,1,20.00,20.00\n"
        "2024-01-02,ORD-2,Cable,Accessories,South,1,10.00,10.00\n"
    )
    df = sales.load_sales(write_csv(tmp_path, text))
    assert sales.total_orders(df) == 2


def test_total_orders_real_file():
    df = sales.load_sales()
    assert sales.total_orders(df) == 482


def test_totals_on_headers_only_file_are_zero(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, HEADER))
    assert sales.total_sales(df) == 0
    assert sales.total_orders(df) == 0
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `venv/bin/python -m pytest -v`
Expected: the 7 new tests FAIL with `AttributeError: module 'sales' has no attribute 'total_sales'` (or `'total_orders'`). The 6 earlier tests still pass.

- [ ] **Step 3: Add the functions to `sales.py`**

Append to `sales.py`:

```python


def total_sales(df):
    """Return total revenue (sum of total_amount), rounded to cents."""
    return round(float(df["total_amount"].sum()), 2)


def total_orders(df):
    """Return the number of orders, counting each order_id once."""
    return int(df["order_id"].nunique())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `venv/bin/python -m pytest -v`
Expected: 13 passed.

- [ ] **Step 5: Commit**

```bash
git add sales.py tests/test_sales.py
git commit -m "TASK-3: add total_sales and total_orders with tests"
```

---

### Task 5 [TASK-3]: KPI cards

**Files:**
- Modify: `app.py` (replace the whole file)

**Interfaces:**
- Consumes: `sales.total_sales(df)`, `sales.total_orders(df)` (Task 4); `get_sales_data()` and `df` (Task 3)
- Produces: two `st.metric` cards labelled "Total Sales" and "Total Orders"

- [ ] **Step 1: Replace `app.py`**

```python
"""ShopSmart Sales Dashboard.

Shows total sales, total orders, the monthly sales trend, and sales by
category and region, all calculated in sales.py from data/sales-data.csv.

Run locally with:  streamlit run app.py
"""
import streamlit as st

import sales

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales_data():
    """Load the sales CSV once and reuse it every time the page reruns."""
    return sales.load_sales(sales.DATA_PATH)


st.title("ShopSmart Sales Dashboard")

# Show a plain message instead of a traceback if the data can't be loaded.
try:
    df = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

if df.empty:
    st.warning("The sales data file has no rows to show.")
    st.stop()

st.caption(f"Sales from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")

# --- KPI cards ---
kpi_sales, kpi_orders = st.columns(2)
kpi_sales.metric("Total Sales", f"${sales.total_sales(df):,.0f}")
kpi_orders.metric("Total Orders", f"{sales.total_orders(df):,}")

# --- Sales trend ---
st.subheader("Sales Trend Over Time")

# --- Breakdowns ---
left, right = st.columns(2)
with left:
    st.subheader("Sales by Category")
with right:
    st.subheader("Sales by Region")
```

- [ ] **Step 2: Smoke-check the page**

Run the smoke check command from the top of this plan.
Expected: `exceptions: []`, `errors: []`, `metrics: [('Total Sales', '$116,500'), ('Total Orders', '482')]`.

- [ ] **Step 3: Owner check in the browser**

Start the app in the background: `venv/bin/streamlit run app.py --server.headless true`
Tell the owner to open http://localhost:8501 and confirm two side-by-side cards: **Total Sales $116,500** and **Total Orders 482**. Wait for their confirmation, then stop the server.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-3: show Total Sales and Total Orders KPI cards"
```

---

### Task 6 [TASK-4]: `sales_by_month`

**Files:**
- Modify: `sales.py` (append one function)
- Test: `tests/test_sales.py` (append tests)

**Interfaces:**
- Consumes: `sales.load_sales`, `sales.total_sales`, and in the tests `SMALL_CSV`, `HEADER`, `write_csv`
- Produces: `sales.sales_by_month(df) -> DataFrame` with columns `month` (datetime, first day of each month) and `sales` (float, rounded to cents), in chronological order, with every month between the first and last present (months with no sales show 0.0)

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales.py`:

```python
# --- sales_by_month ----------------------------------------------------------

def test_sales_by_month_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    result = sales.sales_by_month(df)
    assert list(result.columns) == ["month", "sales"]
    assert list(result["month"].dt.strftime("%Y-%m")) == ["2024-01", "2024-02", "2024-03"]
    assert list(result["sales"]) == [520.00, 80.00, 700.00]


def test_sales_by_month_fills_missing_months_with_zero(tmp_path):
    text = HEADER + (
        "2024-01-10,ORD-1,Laptop,Electronics,North,1,500.00,500.00\n"
        "2024-03-10,ORD-2,Laptop,Electronics,North,1,500.00,500.00\n"
    )
    df = sales.load_sales(write_csv(tmp_path, text))
    result = sales.sales_by_month(df)
    assert list(result["month"].dt.strftime("%Y-%m")) == ["2024-01", "2024-02", "2024-03"]
    assert list(result["sales"]) == [500.00, 0.00, 500.00]


def test_sales_by_month_real_file():
    df = sales.load_sales()
    result = sales.sales_by_month(df)
    assert len(result) == 12
    assert result["month"].is_monotonic_increasing
    assert result["sales"].sum() == pytest.approx(sales.total_sales(df), abs=0.01)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `venv/bin/python -m pytest -v`
Expected: the 3 new tests FAIL with `AttributeError: module 'sales' has no attribute 'sales_by_month'`. The 13 earlier tests still pass.

- [ ] **Step 3: Add the function to `sales.py`**

Append to `sales.py`:

```python


def sales_by_month(df):
    """Return total sales per calendar month, oldest first.

    Columns: month (first day of the month) and sales. Months with no
    orders are included with 0 so the trend line doesn't skip them.
    """
    monthly = df.set_index("date")["total_amount"].resample("MS").sum()
    result = monthly.reset_index()
    result.columns = ["month", "sales"]
    result["sales"] = result["sales"].round(2)
    return result
```

(`"MS"` means "month start": every month is labelled by its first day, and `resample` fills months with no orders with 0.)

- [ ] **Step 4: Run the tests to verify they pass**

Run: `venv/bin/python -m pytest -v`
Expected: 16 passed.

- [ ] **Step 5: Commit**

```bash
git add sales.py tests/test_sales.py
git commit -m "TASK-4: add sales_by_month with tests"
```

---

### Task 7 [TASK-4]: Sales trend line chart

**Files:**
- Modify: `app.py` (replace the whole file)
- Modify: `requirements.txt` only if Step 2 shows a missing package (normally unchanged)

**Interfaces:**
- Consumes: `sales.sales_by_month(df)` (Task 6)
- Produces: one Plotly line chart under "Sales Trend Over Time"

- [ ] **Step 1: Replace `app.py`**

```python
"""ShopSmart Sales Dashboard.

Shows total sales, total orders, the monthly sales trend, and sales by
category and region, all calculated in sales.py from data/sales-data.csv.

Run locally with:  streamlit run app.py
"""
import plotly.express as px
import streamlit as st

import sales

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales_data():
    """Load the sales CSV once and reuse it every time the page reruns."""
    return sales.load_sales(sales.DATA_PATH)


st.title("ShopSmart Sales Dashboard")

# Show a plain message instead of a traceback if the data can't be loaded.
try:
    df = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

if df.empty:
    st.warning("The sales data file has no rows to show.")
    st.stop()

st.caption(f"Sales from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")

# --- KPI cards ---
kpi_sales, kpi_orders = st.columns(2)
kpi_sales.metric("Total Sales", f"${sales.total_sales(df):,.0f}")
kpi_orders.metric("Total Orders", f"{sales.total_orders(df):,}")

# --- Sales trend ---
st.subheader("Sales Trend Over Time")
trend = px.line(sales.sales_by_month(df), x="month", y="sales", markers=True)
trend.update_traces(hovertemplate="%{x|%B %Y}: $%{y:,.2f}<extra></extra>")
trend.update_xaxes(title="Month", tickformat="%b", dtick="M1")
trend.update_yaxes(title="Sales ($)", tickprefix="$", tickformat=",.0f")
st.plotly_chart(trend)

# --- Breakdowns ---
left, right = st.columns(2)
with left:
    st.subheader("Sales by Category")
with right:
    st.subheader("Sales by Region")
```

What the chart settings do: `markers=True` puts a dot on each month. `tickformat="%b"` with `dtick="M1"` labels every month Jan, Feb, …. The `hovertemplate` shows e.g. `March 2024: $10,234.56`, and `<extra></extra>` hides Plotly's extra trace-name box.

- [ ] **Step 2: Smoke-check the page**

Run the smoke check command from the top of this plan.
Expected: `exceptions: []`, `errors: []`, `plotly charts: 1`.

- [ ] **Step 3: Owner check in the browser**

Start the app in the background: `venv/bin/streamlit run app.py --server.headless true`
Tell the owner to open http://localhost:8501 and confirm a full-width line chart with 12 points labelled Jan–Dec, axes "Month" and "Sales ($)", and a hover showing the month and exact dollar amount. Wait for their confirmation, then stop the server.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-4: add monthly sales trend line chart"
```

---

### Task 8 [TASK-5]: `sales_by_category` and `sales_by_region`

**Files:**
- Modify: `sales.py` (append a helper and two functions)
- Test: `tests/test_sales.py` (append tests)

**Interfaces:**
- Consumes: `sales.load_sales`, and in the tests `SMALL_CSV`, `HEADER`, `write_csv`
- Produces:
  - `sales.sales_by_category(df) -> DataFrame` with columns `category`, `sales`, highest first
  - `sales.sales_by_region(df) -> DataFrame` with columns `region`, `sales`, highest first
  - a private helper, `sales._sales_by(df, column)`, that both call

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_sales.py`:

```python
# --- sales_by_category / sales_by_region ------------------------------------

def test_sales_by_category_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    result = sales.sales_by_category(df)
    assert list(result.columns) == ["category", "sales"]
    assert list(result["category"]) == ["Electronics", "Wearables", "Audio", "Accessories"]
    assert list(result["sales"]) == [1000.00, 200.00, 80.00, 20.00]


def test_sales_by_region_small_file(tmp_path):
    df = sales.load_sales(write_csv(tmp_path, SMALL_CSV))
    result = sales.sales_by_region(df)
    assert list(result.columns) == ["region", "sales"]
    assert list(result["region"]) == ["North", "West", "East", "South"]
    assert list(result["sales"]) == [580.00, 500.00, 200.00, 20.00]


def test_sales_by_category_real_file():
    df = sales.load_sales()
    result = sales.sales_by_category(df)
    assert dict(zip(result["category"], result["sales"])) == {
        "Electronics": 42683.67,
        "Wearables": 23698.23,
        "Audio": 19638.44,
        "Smart Home": 19317.23,
        "Accessories": 11162.64,
    }
    assert result["category"].iloc[0] == "Electronics"


def test_sales_by_region_real_file():
    df = sales.load_sales()
    result = sales.sales_by_region(df)
    assert list(result["region"]) == ["North", "West", "East", "South"]
    assert list(result["sales"]) == [38857.24, 27463.74, 26783.53, 23395.70]


def test_breakdowns_are_rounded_to_cents(tmp_path):
    text = HEADER + (
        "2024-01-01,ORD-1,Cable,Accessories,North,1,0.10,0.10\n"
        "2024-01-02,ORD-2,Cable,Accessories,North,1,0.20,0.20\n"
    )
    df = sales.load_sales(write_csv(tmp_path, text))
    assert list(sales.sales_by_category(df)["sales"]) == [0.30]
    assert list(sales.sales_by_region(df)["sales"]) == [0.30]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `venv/bin/python -m pytest -v`
Expected: the 5 new tests FAIL with `AttributeError: module 'sales' has no attribute 'sales_by_category'` (or `'sales_by_region'`). The 16 earlier tests still pass.

- [ ] **Step 3: Add the functions to `sales.py`**

Append to `sales.py`:

```python


def _sales_by(df, column):
    """Return total sales per value of `column`, highest first.

    Shared by sales_by_category and sales_by_region.
    """
    grouped = df.groupby(column, as_index=False)["total_amount"].sum()
    grouped = grouped.rename(columns={"total_amount": "sales"})
    grouped["sales"] = grouped["sales"].round(2)
    return grouped.sort_values("sales", ascending=False, ignore_index=True)


def sales_by_category(df):
    """Return total sales per product category, highest first."""
    return _sales_by(df, "category")


def sales_by_region(df):
    """Return total sales per region, highest first."""
    return _sales_by(df, "region")
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `venv/bin/python -m pytest -v`
Expected: 21 passed.

- [ ] **Step 5: Commit**

```bash
git add sales.py tests/test_sales.py
git commit -m "TASK-5: add sales_by_category and sales_by_region with tests"
```

---

### Task 9 [TASK-5]: Category and region bar charts

**Files:**
- Modify: `app.py` (replace the whole file)

**Interfaces:**
- Consumes: `sales.sales_by_category(df)`, `sales.sales_by_region(df)` (Task 8)
- Produces: in `app.py`, a `bar_chart(table, label_column)` helper and two horizontal Plotly bar charts. This is the final `app.py`.

- [ ] **Step 1: Replace `app.py`**

```python
"""ShopSmart Sales Dashboard.

Shows total sales, total orders, the monthly sales trend, and sales by
category and region, all calculated in sales.py from data/sales-data.csv.

Run locally with:  streamlit run app.py
"""
import plotly.express as px
import streamlit as st

import sales

BAR_COLOR = "#1f77b4"  # one consistent color for both bar charts

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales_data():
    """Load the sales CSV once and reuse it every time the page reruns."""
    return sales.load_sales(sales.DATA_PATH)


def bar_chart(table, label_column):
    """Draw a horizontal bar chart of sales per label, biggest bar on top."""
    fig = px.bar(table, x="sales", y=label_column, orientation="h")
    fig.update_traces(marker_color=BAR_COLOR, hovertemplate="%{y}: $%{x:,.2f}<extra></extra>")
    fig.update_xaxes(title="Sales ($)", tickprefix="$", tickformat=",.0f")
    # Plotly draws horizontal bars bottom-up, so "total ascending" puts the biggest on top.
    fig.update_yaxes(title=None, categoryorder="total ascending")
    return fig


st.title("ShopSmart Sales Dashboard")

# Show a plain message instead of a traceback if the data can't be loaded.
try:
    df = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load sales data: {error}")
    st.stop()

if df.empty:
    st.warning("The sales data file has no rows to show.")
    st.stop()

st.caption(f"Sales from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")

# --- KPI cards ---
kpi_sales, kpi_orders = st.columns(2)
kpi_sales.metric("Total Sales", f"${sales.total_sales(df):,.0f}")
kpi_orders.metric("Total Orders", f"{sales.total_orders(df):,}")

# --- Sales trend ---
st.subheader("Sales Trend Over Time")
trend = px.line(sales.sales_by_month(df), x="month", y="sales", markers=True)
trend.update_traces(hovertemplate="%{x|%B %Y}: $%{y:,.2f}<extra></extra>")
trend.update_xaxes(title="Month", tickformat="%b", dtick="M1")
trend.update_yaxes(title="Sales ($)", tickprefix="$", tickformat=",.0f")
st.plotly_chart(trend)

# --- Breakdowns ---
left, right = st.columns(2)
with left:
    st.subheader("Sales by Category")
    st.plotly_chart(bar_chart(sales.sales_by_category(df), "category"))
with right:
    st.subheader("Sales by Region")
    st.plotly_chart(bar_chart(sales.sales_by_region(df), "region"))
```

- [ ] **Step 2: Smoke-check the page**

Run the smoke check command from the top of this plan.
Expected: `exceptions: []`, `errors: []`, `plotly charts: 3`.

- [ ] **Step 3: Owner check in the browser**

Start the app in the background: `venv/bin/streamlit run app.py --server.headless true`
Tell the owner to open http://localhost:8501 and confirm:
- Left: "Sales by Category", horizontal bars from the top: Electronics, Wearables, Audio, Smart Home, Accessories.
- Right: "Sales by Region", horizontal bars from the top: North, West, East, South.
- Both bar charts are the same color, and hovering shows the exact dollar amount.

Wait for their confirmation, then stop the server.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-5: add category and region bar charts"
```

---

### Task 10 [TASK-6]: Verify every acceptance criterion and polish

**Files:**
- Modify: `sales.py`, `app.py`, `tests/test_sales.py` only if a check below fails

**Interfaces:**
- Consumes: everything above
- Produces: a verified, warning-free app ready to merge

- [ ] **Step 1: Run the full test suite with warnings treated as errors**

Run: `venv/bin/python -m pytest -v -W error`
Expected: 21 passed, with no warnings. If a `FutureWarning` or `DeprecationWarning` from **our** code (`sales.py` or the tests) turns into an error, fix the call it points to (keeping behavior the same), re-run, and note the fix for the commit. If the warning comes from inside a third-party package (the traceback ends in `venv/lib/...`), don't change any code: report it to the owner and re-run without `-W error` to confirm 21 passed.

- [ ] **Step 2: Cross-check the numbers without pandas**

This recomputes the reference values with Python's built-in `csv` module, independent of `sales.py`:

```bash
venv/bin/python - <<'EOF'
import csv
from collections import defaultdict

rows = list(csv.DictReader(open("data/sales-data.csv")))
print("orders:", len({r["order_id"] for r in rows}))
print("total:", round(sum(float(r["total_amount"]) for r in rows), 2))
for column in ("category", "region"):
    totals = defaultdict(float)
    for r in rows:
        totals[r[column]] += float(r["total_amount"])
    print(column, sorted(((round(v, 2), k) for k, v in totals.items()), reverse=True))
EOF
```

Expected: `orders: 482`, `total: 116500.21`, and category and region totals matching the reference values table at the top of this plan. Then run the smoke check command and confirm its metrics show `$116,500` and `482`.

- [ ] **Step 3: Check the load time and that the page has no exceptions**

Run the smoke check command from the top of this plan.
Expected: `run time:` under `5.00s` (NFR-1), `exceptions: []`, `errors: []`, `metrics: [('Total Sales', '$116,500'), ('Total Orders', '482')]`, `plotly charts: 3`.

- [ ] **Step 4: Check the server log for warnings**

Start the app in the background with its output saved: `venv/bin/streamlit run app.py --server.headless true > streamlit.log 2>&1`
Ask the owner to open http://localhost:8501 once so the page actually renders. Then run:

`grep -i -E "warning|deprecat|traceback|error" streamlit.log || echo "log clean"`

Expected: `log clean`. If anything matches, fix what it points to (e.g. a deprecated Streamlit argument) and repeat this step. Stop the server and delete the log: `rm streamlit.log`.

- [ ] **Step 5: Owner walks the PRD acceptance checklist**

Start the app again in the background: `venv/bin/streamlit run app.py --server.headless true`
Ask the owner to confirm each item on http://localhost:8501:
- [ ] **KPIs visible:** Total Sales $116,500 and Total Orders 482, shown prominently
- [ ] **Trend chart works:** 12 monthly points, Jan–Dec 2024, with exact values on hover
- [ ] **Category chart works:** sorted highest to lowest, Electronics on top
- [ ] **Region chart works:** sorted highest to lowest, North on top
- [ ] **Data loads correctly:** matches Step 2
- [ ] **No errors:** nothing red on the page, and the browser console is clean
- [ ] **Professional appearance:** labels readable, nothing overlapping, suitable for an executive meeting

Fix anything the owner flags, then repeat Steps 1 and 3. Stop the server.

- [ ] **Step 6: Readability pass**

Re-read `sales.py` and `app.py` and confirm:
- every function has a docstring
- there are no unused imports
- `sales.py` does not import `streamlit` or `plotly` (check with `grep -n -E "streamlit|plotly" sales.py`, which should print nothing)
- `git status --short` shows no `venv/`, `__pycache__/`, `.pytest_cache/`, or `streamlit.log`

- [ ] **Step 7: Commit (only if Steps 1–6 changed anything)**

If `git status --short` shows changes:

```bash
git add sales.py app.py tests/test_sales.py
git commit -m "TASK-6: polish after acceptance review"
```

If nothing changed, skip the commit and tell the owner TASK-6 passed with no changes, so its Commit line can point to the last TASK-5 commit.

---

### Task 11 [TASK-7]: Hand-off. **Owner executes deployment.**

**Implementation stops here.** The agent does not merge, push, or deploy. It reports to the owner and ends:

- [ ] **Step 1: Final status report to the owner**

Run and show the output of:

```bash
git status --short --branch
git log --oneline main..HEAD
venv/bin/python -m pytest -q
```

Expected: on `feature/sales-dashboard` with a clean working tree; one commit per plan task (each starting with its TASK-N ID, TASK-6 possibly absent); `21 passed`.

- [ ] **Step 2: Hand off with the owner's deployment checklist**

Tell the owner the build is complete and list what's theirs to do:

1. Update `TASKS.md` for any milestones not yet moved to Done (check off criteria, fill in the Commit lines).
2. Merge `feature/sales-dashboard` into `main` and push to GitHub.
3. On Streamlit Community Cloud, deploy from repo branch **`main`** with main file **`app.py`**. Under *Advanced settings*, choose the Python version closest to the local one (`venv/bin/python --version`). The pins in `requirements.txt` were resolved on that version.
4. Open the public URL and confirm it shows the same values as the local app ($116,500 and 482, with Electronics and North on top).
5. Record the live URL on TASK-7 in `TASKS.md` and move TASK-7 to Done.

Then stop. Do not take any of these steps unless the owner explicitly asks.
