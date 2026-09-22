# Tasks

This file tracks all work for the ShopSmart Sales Dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

A milestone moves to Done only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message (e.g. `TASK-3: add KPI cards`)

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard so stakeholders can view it at a public URL (NFR-5).
- [ ] App is deployed on Streamlit Community Cloud and loads from a public shareable URL
- [ ] The deployed app shows the same values as the local version

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python environment and project skeleton for the Streamlit app.
- [x] `requirements.txt` lists Streamlit, Plotly, and Pandas, and installs cleanly on Python 3.11+
- [x] `app.py` exists and `streamlit run app.py` opens a page with the dashboard title

Commit: 9c3e1b8
Notes: `python3 -m venv` refused to run because the project folder was named `~:Github` (the colon breaks PATH); I renamed it to `~/Github`. Used the plan's commit message ("set up venv, pinned requirements, and app stub") instead of the tutorial's example, since no data loading was in this milestone. Claude committed before I'd confirmed the page in the browser.

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` with Pandas and set up the dashboard's page layout.
- [x] CSV loads with `date` parsed as a date and `quantity`, `unit_price`, `total_amount` as numeric columns
- [x] Loaded data has 482 rows, 5 categories, and 4 regions
- [x] Page layout has sections for KPIs, trend chart, and category/region charts

Commit: cb057bc
Notes: Trend and category/region sections are on the page; the KPI row has no heading of its own and lands in TASK-3, per the design. Claude added a test the plan didn't have (numeric columns, 5 categories, 4 regions) so these criteria are actually checked (7 tests instead of 6). I chose the commit message "set up project and data loading". Claude again committed before I'd confirmed the page in the browser.

### TASK-3: KPI cards implementation
Show Total Sales and Total Orders at the top of the dashboard (FR-1).
- [x] Total Sales is shown as currency (`$X,XXX,XXX`) and is about $116,500
- [x] Total Orders is shown with thousands separators and equals 482

Commit: 5876df5
Notes: Claude did the browser check itself in headless Chrome (screenshot showed $116,500 and 482 side by side, no errors) rather than me looking; its first headless screenshot only caught Streamlit's loading skeleton, so it wrote a DevTools driver to wait for the cards. 14 tests instead of the plan's 13, because of the extra TASK-2 test.

### TASK-4: Sales trend chart
Add an interactive Plotly line chart of sales over time (FR-2).
- [x] Line chart shows sales by month (or day) with time on the X-axis and sales amount on the Y-axis
- [x] Hover tooltips show exact values, and axes and title are clearly labeled

Commit: 24b01cc
Notes: Claude did the browser check in headless Chrome on port 8502, because a server left over from TASK-3 was still running on 8501. The chart shows 12 points labelled Jan-Dec with axes "Month" and "Sales ($)", and the hover values (e.g. March 2024: $9,603.10) match sums taken straight from the CSV. There were no console errors. The chart's title is the "Sales Trend Over Time" section heading, per the design. 17 tests (the plan's 16, +1 from TASK-2).

### TASK-5: Category and region breakdowns
Add side-by-side bar charts for sales by category and by region (FR-3, FR-4).
- [x] Category chart shows all 5 categories sorted highest to lowest, with Electronics on top
- [x] Region chart shows North, South, East, and West sorted highest to lowest
- [x] Both charts have hover tooltips with exact values

Commit: b95ddc5
Notes: Claude did the browser check in headless Chrome. Category bars run top to bottom Electronics, Wearables, Audio, Smart Home, Accessories. Region bars run North, West, East, South, which is highest to lowest; the criterion's list only names the regions. Both charts use the same blue, and the hover values (e.g. Electronics: $42,683.67, North: $38,857.24) match the plan's reference values. There were no console errors. 22 tests (the plan's 21, +1 from TASK-2).

### TASK-6: Testing and refinement
Check the dashboard against the PRD's acceptance criteria and polish it for executive use.
- [x] All displayed values match calculations done directly on the CSV
- [x] Dashboard runs with no errors or warnings in the terminal or browser
- [x] Dashboard loads within 5 seconds and has consistent, professional styling

Commit: 3d0582d
Notes: Claude checked everything itself: 22 tests pass with warnings treated as errors; the values match a separate recomputation with Python's csv module (482 orders, $116,500.21, every category and region); the page runs in about 0.6s (under 5s); the Streamlit log is clean; there are no console errors. One polish fix: the trend line was Streamlit's default light blue while the bars were #1f77b4, so all three charts now share one color (BAR_COLOR renamed CHART_COLOR). The owner-checklist walkthrough was done by Claude in headless Chrome, not by me in a browser.
