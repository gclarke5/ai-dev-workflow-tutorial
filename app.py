"""ShopSmart Sales Dashboard.

Shows total sales, total orders, the monthly sales trend, and sales by
category and region, all calculated in sales.py from data/sales-data.csv.

Run locally with:  streamlit run app.py
"""
import plotly.express as px
import streamlit as st

import sales

CHART_COLOR = "#1f77b4"  # one consistent color for every chart

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales_data():
    """Load the sales CSV once and reuse it every time the page reruns."""
    return sales.load_sales(sales.DATA_PATH)


def bar_chart(table, label_column):
    """Draw a horizontal bar chart of sales per label, biggest bar on top."""
    fig = px.bar(table, x="sales", y=label_column, orientation="h")
    fig.update_traces(marker_color=CHART_COLOR, hovertemplate="%{y}: $%{x:,.2f}<extra></extra>")
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
trend.update_traces(line_color=CHART_COLOR, hovertemplate="%{x|%B %Y}: $%{y:,.2f}<extra></extra>")
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
