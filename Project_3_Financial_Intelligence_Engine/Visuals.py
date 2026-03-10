import plotly.express as px


def budget_vs_actual_chart(df):

    fig = px.bar(
        df,
        x="category",
        y=["budget","actual"],
        barmode="group",
        title="Budget vs Actual Spending"
    )

    return fig


def expense_mix_chart(df):

    fig = px.pie(
        df,
        names="category",
        values="actual",
        title="Expense Distribution"
    )

    return fig
