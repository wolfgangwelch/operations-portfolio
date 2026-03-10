import plotly.express as px

def revenue_trend_chart(df):

    fig = px.line(
        df,
        x="date",
        y="revenue",
        title="Revenue Trend"
    )

    return fig


def category_distribution_chart(df):

    fig = px.pie(
        df,
        names="category",
        values="share",
        title="Revenue Distribution"
    )

    return fig
