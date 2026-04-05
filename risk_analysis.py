import numpy as np
import pandas as pd


# ------------------------------
# Calculate daily returns
# ------------------------------
def calculate_returns(df):

    df["Returns"] = df["Close"].pct_change()

    return df


# ------------------------------
# Volatility Calculation
# ------------------------------
def calculate_volatility(df):

    returns = df["Returns"].dropna()

    volatility = np.std(returns) * np.sqrt(252)

    return volatility


# ------------------------------
# Expected Return
# ------------------------------
def expected_return(df):

    returns = df["Returns"].dropna()

    return np.mean(returns) * 252


# ------------------------------
# Sharpe Ratio
# ------------------------------
def sharpe_ratio(df, risk_free_rate=0.03):

    returns = df["Returns"].dropna()

    excess_returns = returns - risk_free_rate / 252

    sharpe = np.mean(excess_returns) / np.std(returns)

    sharpe = sharpe * np.sqrt(252)

    return sharpe


# ------------------------------
# Risk Level Classification
# ------------------------------
def risk_level(volatility):

    if volatility < 0.20:
        return "Low Risk"

    elif volatility < 0.40:
        return "Medium Risk"

    else:
        return "High Risk"


# ------------------------------
# Investment Simulation
# ------------------------------
def simulate_investment(investment, current_price, predicted_price):

    shares = investment / current_price

    future_value = shares * predicted_price

    profit = future_value - investment

    profit_percent = (profit / investment) * 100

    return {
        "investment": investment,
        "shares_bought": shares,
        "future_value": future_value,
        "profit": profit,
        "profit_percent": profit_percent
    }


# ------------------------------
# Full Risk Report
# ------------------------------
def generate_risk_report(df):

    df = calculate_returns(df)

    vol = calculate_volatility(df)

    exp_return = expected_return(df)

    sharpe = sharpe_ratio(df)

    level = risk_level(vol)

    return {
        "volatility": vol,
        "expected_return": exp_return,
        "sharpe_ratio": sharpe,
        "risk_level": level
    }