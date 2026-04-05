import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go


def plot_candlestick(df):

    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=500
    )

    return fig


def plot_prediction(df, predicted_prices):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name='Actual Price'
    ))

    future_dates = df['Date'].iloc[-len(predicted_prices):]

    fig.add_trace(go.Scatter(
        x=future_dates,
        y=predicted_prices,
        mode='lines',
        name='Predicted Price'
    ))

    fig.update_layout(
        title="Stock Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark",
        height=500
    )

    return fig


def plot_stock_comparison(stock_data):

    fig = go.Figure()

    for stock, df in stock_data.items():
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name=stock
            )
        )

    fig.update_layout(
        title="Stock Price Comparison",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    return fig