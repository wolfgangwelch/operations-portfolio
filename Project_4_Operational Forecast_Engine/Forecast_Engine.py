import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def build_forecast(df):

    df = df.sort_values("date")

    df["day_index"] = range(len(df))

    X = df[["day_index"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    future_index = np.array([[len(df)+i] for i in range(30)])

    forecast = model.predict(future_index)

    future_dates = pd.date_range(df["date"].max(), periods=30)

    forecast_df = pd.DataFrame({
        "date":future_dates,
        "forecast_revenue":forecast
    })

    return forecast_df


def growth_rate(df):

    start = df["revenue"].iloc[0]
    end = df["revenue"].iloc[-1]

    growth = ((end-start)/start)*100

    return growth


def volatility_signal(df):

    volatility = df["revenue"].std()

    if volatility > df["revenue"].mean()*0.25:

        return "⚠ Revenue volatility increasing"

    return None
