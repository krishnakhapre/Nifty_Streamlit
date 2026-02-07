import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Stock Market Interactive Dashboard")
st.markdown("Analyze stock price movements with technical indicators")

# ----------------------------------
# Load Data
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_NS.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df

df = load_data()

# ----------------------------------
# Sidebar Controls
# ----------------------------------
st.sidebar.header("🔎 Filters")

stock = st.sidebar.selectbox(
    "Select Stock",
    df["Stock"].unique()
)

stock_df = df[df["Stock"] == stock]

start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(stock_df.Date.min(), stock_df.Date.max()),
    min_value=stock_df.Date.min(),
    max_value=stock_df.Date.max()
)

stock_df = stock_df[
    (stock_df["Date"] >= pd.to_datetime(start_date)) &
    (stock_df["Date"] <= pd.to_datetime(end_date))
]

st.sidebar.header("📐 Indicators")
ma20 = st.sidebar.checkbox("20 Day Moving Average", True)
ma50 = st.sidebar.checkbox("50 Day Moving Average")
ma200 = st.sidebar.checkbox("200 Day Moving Average")

show_volume = st.sidebar.checkbox("Show Volume", True)

# ----------------------------------
# Metrics
# ----------------------------------
latest = stock_df.iloc[-1]
prev = stock_df.iloc[-2] if len(stock_df) > 1 else latest

price_change = latest.Close - prev.Close
pct_change = (price_change / prev.Close) * 100 if prev.Close != 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Last Close", f"₹{latest.Close:.2f}", f"{pct_change:.2f}%")
c2.metric("High", f"₹{stock_df.High.max():.2f}")
c3.metric("Low", f"₹{stock_df.Low.min():.2f}")
c4.metric("Volatility", f"{stock_df.Close.pct_change().std()*100:.2f}%")

# ----------------------------------
# Candlestick Chart
# ----------------------------------
fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=stock_df["Date"],
    open=stock_df["Open"],
    high=stock_df["High"],
    low=stock_df["Low"],
    close=stock_df["Close"],
    name="Price"
))

if ma20:
    stock_df["MA20"] = stock_df.Close.rolling(20).mean()
    fig.add_trace(go.Scatter(
        x=stock_df.Date,
        y=stock_df.MA20,
        line=dict(color="orange"),
        name="MA 20"
    ))

if ma50:
    stock_df["MA50"] = stock_df.Close.rolling(50).mean()
    fig.add_trace(go.Scatter(
        x=stock_df.Date,
        y=stock_df.MA50,
        line=dict(color="blue"),
        name="MA 50"
    ))

if ma200:
    stock_df["MA200"] = stock_df.Close.rolling(200).mean()
    fig.add_trace(go.Scatter(
        x=stock_df.Date,
        y=stock_df.MA200,
        line=dict(color="green"),
        name="MA 200"
    ))

fig.update_layout(
    height=600,
    xaxis_rangeslider_visible=False,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Volume Chart
# ----------------------------------
if show_volume and "Volume" in stock_df.columns:
    st.subheader("📦 Trading Volume")
    vol_fig = go.Figure()
    vol_fig.add_bar(
        x=stock_df.Date,
        y=stock_df.Volume,
        marker_color="purple"
    )
    vol_fig.update_layout(height=250, template="plotly_dark")
    st.plotly_chart(vol_fig, use_container_width=True)

# ----------------------------------
# Data Tools
# ----------------------------------
st.subheader("📥 Data Tools")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Download Filtered Data",
        stock_df.to_csv(index=False),
        file_name=f"{stock}_data.csv"
    )

with col2:
    if st.checkbox("Show Raw Data"):
        st.dataframe(stock_df)

# ----------------------------------
# Footer
# ----------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Plotly")
