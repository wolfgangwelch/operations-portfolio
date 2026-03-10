import plotly.express as px

def revenue_distribution_chart(df):

    fig = px.pie(
        df,
        names="category",
        values="revenue_share",
        title="Revenue Distribution by Category"
    )

    return fig


def growth_chart(df):

    fig = px.bar(
        df,
        x="category",
        y="growth_percent",
        title="Category Growth Comparison"
    )

    return fig
