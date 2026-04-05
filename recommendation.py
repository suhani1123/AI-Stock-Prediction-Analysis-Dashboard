import pandas as pd
import ta


# ---------------------------------------
# Calculate Technical Indicators
# ---------------------------------------
def add_indicators(df):

    # Moving Averages
    df["MA50"] = df["Close"].rolling(window=50).mean()
    df["MA200"] = df["Close"].rolling(window=200).mean()

    # RSI Indicator
    rsi = ta.momentum.RSIIndicator(close=df["Close"], window=14)
    df["RSI"] = rsi.rsi()

    return df


# ---------------------------------------
# Generate Trading Recommendation
# ---------------------------------------
def generate_recommendation(df):

    df = add_indicators(df)

    latest = df.iloc[-1]

    price = latest["Close"]
    ma50 = latest["MA50"]
    ma200 = latest["MA200"]
    rsi = latest["RSI"]

    # Basic Trading Logic
    if price > ma50 and ma50 > ma200 and rsi < 70:
        return "BUY"

    elif price < ma50 and ma50 < ma200 and rsi > 30:
        return "SELL"

    else:
        return "HOLD"


# ---------------------------------------
# Get Indicator Values
# ---------------------------------------
def get_indicator_summary(df):

    df = add_indicators(df)

    latest = df.iloc[-1]

    return {
        "price": round(latest["Close"], 2),
        "MA50": round(latest["MA50"], 2),
        "MA200": round(latest["MA200"], 2),
        "RSI": round(latest["RSI"], 2)
    }