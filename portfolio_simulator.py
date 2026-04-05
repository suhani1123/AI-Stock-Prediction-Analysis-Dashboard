import pandas as pd
import streamlit as st

from risk_analysis import generate_risk_report
from risk_analysis import simulate_investment

# Portfolio Simulation UI

def portfolio_simulator(df, predicted_price):

    st.subheader("💼 Portfolio Investment Simulator")

    # Investment input
    investment = st.number_input(
        "Enter Investment Amount (₹)",
        min_value=1000,
        max_value=1000000,
        step=1000
    )

    current_price = df["Close"].iloc[-1]

    # Run simulation
    if st.button("Simulate Investment"):

        result = simulate_investment(
            investment,
            current_price,
            predicted_price
        )

        risk = generate_risk_report(df)

        st.divider()

        st.subheader("📊 Investment Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current Price",
                f"₹{round(current_price,2)}"
            )

        with col2:
            st.metric(
                "Predicted Price",
                f"₹{round(predicted_price,2)}"
            )

        with col3:
            st.metric(
                "Risk Level",
                risk["risk_level"]
            )

        st.divider()

        st.subheader("💰 Portfolio Performance")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Investment Amount",
                f"₹{result['investment']:.2f}"
            )

            st.metric(
                "Shares Purchased",
                f"{result['shares_bought']:.2f}"
            )

        with col2:

            st.metric(
                "Future Value",
                f"₹{result['future_value']:.2f}"
            )

            st.metric(
                "Expected Profit",
                f"₹{result['profit']:.2f}"
            )

        st.progress(min(int(result["profit_percent"]),100))

        st.write(
            f"Expected Return: **{result['profit_percent']:.2f}%**"
        )

        st.divider()

        st.subheader("📉 Risk Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Volatility",
                f"{risk['volatility']:.2f}"
            )

        with col2:
            st.metric(
                "Expected Return",
                f"{risk['expected_return']:.2f}"
            )

        with col3:
            st.metric(
                "Sharpe Ratio",
                f"{risk['sharpe_ratio']:.2f}"
            )
