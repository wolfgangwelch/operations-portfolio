import plotly.express as px

def revenue_by_location_chart(df):

    fig = px.bar(
        df,
        x="location",
        y="revenue",
        title="Revenue by Location"
    )

    return fig


def growth_chart(df):

    fig = px.bar(
        df,
        x="location",
        y="growth_percent",
        title="Location Growth Comparison"
    )

    return fig
