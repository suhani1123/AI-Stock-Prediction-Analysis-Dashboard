import streamlit as st
import pandas as pd

# Import modules
from data_fetcher import get_stock_data
from charts import plot_candlestick, plot_prediction, plot_stock_comparison
from predictor import train_lstm_model, predict_future_prices
from recommendation import generate_recommendation, get_indicator_summary
from risk_analysis import generate_risk_report
from portfolio_simulator import portfolio_simulator

# -------------------- CONFIG --------------------

st.set_page_config(
    page_title="AI Stock Prediction Dashboard",
    layout="wide"
)

st.title("📈 AI Powered Stock Prediction & Analysis System")
st.markdown("Real-time stock analytics with AI prediction and portfolio simulation")
st.divider()

# -------------------- CACHE FUNCTIONS --------------------

@st.cache_data
def load_data(symbol, period):
    return get_stock_data(symbol, period)

@st.cache_resource
def load_model(df):
    return train_lstm_model(df)

# -------------------- SIDEBAR --------------------

st.sidebar.header("Stock Settings")

stock_symbol = st.sidebar.selectbox(
    "Select Stock Symbol",
    ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "WIPRO.NS", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"]
)

period = st.sidebar.selectbox(
    "Select Time Period",
    ["6mo", "1y", "2y"]  # reduced load
)

compare_stocks = st.sidebar.multiselect(
    "Compare Stocks",
    ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "WIPRO.NS", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"]
)

# -------------------- DATA --------------------

df = load_data(stock_symbol, period)

if df is None or df.empty:
    st.error("Unable to fetch stock data")
    st.stop()

# -------------------- METRICS --------------------

current_price = df["Close"].iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Price", f"₹{current_price:.2f}")

with col2:
    indicators = get_indicator_summary(df)
    st.metric("RSI", indicators["RSI"])

with col3:
    signal = generate_recommendation(df)
    st.metric("Trading Signal", signal)

st.divider()

# -------------------- CHART --------------------

st.subheader("Candlestick Chart 📊")
candlestick_chart = plot_candlestick(df)
st.plotly_chart(candlestick_chart, use_container_width=True)

# -------------------- AI PREDICTION --------------------

st.subheader("AI Price Prediction 🤖")

# Load model (cached)
model, scaler, x_test, y_test = load_model(df)

# Predict
predicted_prices = predict_future_prices(model, scaler, df)

prediction_chart = plot_prediction(df, predicted_prices)
st.plotly_chart(prediction_chart, use_container_width=True)

predicted_price = predicted_prices[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric("Predicted Price (Next Days)", f"₹{predicted_price:.2f}")

with col2:
    change = ((predicted_price - current_price) / current_price) * 100
    st.metric("Expected Change", f"{change:.2f}%")

st.divider()

# -------------------- RISK --------------------

st.subheader("Risk Analysis 📉")
risk = generate_risk_report(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Volatility", f"{risk['volatility']:.2f}")

with col2:
    st.metric("Expected Return", f"{risk['expected_return']:.2f}")

with col3:
    st.metric("Sharpe Ratio", f"{risk['sharpe_ratio']:.2f}")

with col4:
    st.metric("Risk Level", risk["risk_level"])

st.divider()

# -------------------- PORTFOLIO --------------------

portfolio_simulator(df, predicted_price)

st.divider()

# -------------------- COMPARISON --------------------

st.subheader("Stock Comparison 📊")

if len(compare_stocks) > 0:
    stock_data = {}

    for stock in compare_stocks:
        stock_data[stock] = load_data(stock, period)

    comparison_chart = plot_stock_comparison(stock_data)
    st.plotly_chart(comparison_chart, use_container_width=True)

else:
    st.info("Select at least one stock to compare.")

# -------------------- FOOTER --------------------

st.markdown("""---  
### END  
""")
