# Tasks

This file tracks all work for the ShopSmart Sales Dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

A milestone moves to Done only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message (e.g. `TASK-3: add KPI cards`)

## To Do

### TASK-3: KPI cards implementation
Show Total Sales and Total Orders at the top of the dashboard (FR-1).
- [ ] Total Sales is shown as currency (`$X,XXX,XXX`) and is about $116,500
- [ ] Total Orders is shown with thousands separators and equals 482

Commit:

### TASK-4: Sales trend chart
Add an interactive Plotly line chart of sales over time (FR-2).
- [ ] Line chart shows sales by month (or day) with time on the X-axis and sales amount on the Y-axis
- [ ] Hover tooltips show exact values, and axes and title are clearly labeled

Commit:

### TASK-5: Category and region breakdowns
Add side-by-side bar charts for sales by category and by region (FR-3, FR-4).
- [ ] Category chart shows all 5 categories sorted highest to lowest, with Electronics on top
- [ ] Region chart shows North, South, East, and West sorted highest to lowest
- [ ] Both charts have hover tooltips with exact values

Commit:

### TASK-6: Testing and refinement
Check the dashboard against the PRD's acceptance criteria and polish it for executive use.
- [ ] All displayed values match calculations done directly on the CSV
- [ ] Dashboard runs with no errors or warnings in the terminal or browser
- [ ] Dashboard loads within 5 seconds and has consistent, professional styling

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard so stakeholders can view it at a public URL (NFR-5).
- [ ] App is deployed on Streamlit Community Cloud and loads from a public shareable URL
- [ ] The deployed app shows the same values as the local version

Commit:

## In Progress

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` with Pandas and set up the dashboard's page layout.
- [ ] CSV loads with `date` parsed as a date and `quantity`, `unit_price`, `total_amount` as numeric columns
- [ ] Loaded data has 482 rows, 5 categories, and 4 regions
- [ ] Page layout has sections for KPIs, trend chart, and category/region charts

Commit:

## Done

### TASK-1: Environment setup and project initialization
Set up the Python environment and project skeleton for the Streamlit app.
- [x] `requirements.txt` lists Streamlit, Plotly, and Pandas, and installs cleanly on Python 3.11+
- [x] `app.py` exists and `streamlit run app.py` opens a page with the dashboard title

Commit: 9c3e1b8
Notes: `python3 -m venv` refused to run because the project folder was named `~:Github` (the colon breaks PATH); I renamed it to `~/Github`. Used the plan's commit message ("set up venv, pinned requirements, and app stub") instead of the tutorial's example, since no data loading was in this milestone. Claude committed before I'd confirmed the page in the browser.
