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
