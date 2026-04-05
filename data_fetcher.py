import yfinance as yf
import pandas as pd


def get_stock_data(symbol, period="1y"):
    """
    Fetch historical stock data using Yahoo Finance API
    """

    ticker = yf.Ticker(symbol)

    df = ticker.history(period=period)

    df.reset_index(inplace=True)

    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    return df


def get_current_price(symbol):
    """
    Fetch latest market price
    """

    ticker = yf.Ticker(symbol)

    data = ticker.history(period="1d")

    return float(data["Close"].iloc[-1])