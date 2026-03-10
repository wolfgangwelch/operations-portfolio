import plotly.graph_objects as go


def forecast_chart(history, forecast):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history["date"],
            y=history["revenue"],
            name="Historical Revenue"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["forecast_revenue"],
            name="Forecast"
        )
    )

    return fig
