import plotly.express as px

def category_efficiency_chart(df):

    fig = px.bar(
        df,
        x="category",
        y="revenue_per_unit",
        title="Revenue Efficiency by Category"
    )

    return fig
