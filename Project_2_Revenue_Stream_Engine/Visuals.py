import plotly.express as px


def revenue_mix_chart(category_df):

    fig = px.pie(
        category_df,
        names="category",
        values="revenue",
        title="Revenue Mix"
    )

    return fig


def category_bar_chart(category_df):

    fig = px.bar(
        category_df,
        x="category",
        y="revenue",
        title="Revenue by Category"
    )

    return fig
