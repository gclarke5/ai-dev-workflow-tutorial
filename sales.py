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


def total_sales(df):
    """Return total revenue (sum of total_amount), rounded to cents."""
    return round(float(df["total_amount"].sum()), 2)


def total_orders(df):
    """Return the number of orders, counting each order_id once."""
    return int(df["order_id"].nunique())


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
