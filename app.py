import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import streamlit as st

# Page config
st.set_page_config(page_title="Stock Price Viewer", layout="wide")

st.title("📈 Stock Price Analysis")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_NS.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")

# Stock selector
stock_list = df["Stock"].unique()
st.sidebar.subheader("Select Stock")
st_name = st.sidebar.selectbox("Stock Name", stock_list)

# Filter by stock
r = df[df["Stock"] == st_name]

# Date range selector
min_date = r["Date"].min()
max_date = r["Date"].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply date filter
mask = (r["Date"] >= pd.to_datetime(start_date)) & (r["Date"] <= pd.to_datetime(end_date))
r = r.loc[mask]

# Plot
st.subheader(f"Closing Price Trend — {st_name}")

fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(data=r, x="Date", y="Close", ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
plt.xticks(rotation=45)

st.
