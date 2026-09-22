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


def test_load_sales_real_file_matches_task_2_criteria():
    df = sales.load_sales()
    for column in ["quantity", "unit_price", "total_amount"]:
        assert pd.api.types.is_numeric_dtype(df[column]), column
    assert df["category"].nunique() == 5
    assert df["region"].nunique() == 4


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
