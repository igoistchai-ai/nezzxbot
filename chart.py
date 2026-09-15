import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path
import pandas as pd



def create_chart(
        df,
        symbol,
        timeframe="15m"
):

    df = df.copy()


    # исправляем дату
    if "timestamp" in df.columns:

        if pd.api.types.is_numeric_dtype(
            df["timestamp"]
        ):

            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                unit="ms"
            )

        else:

            df["timestamp"] = pd.to_datetime(
                df["timestamp"]
            )


    elif "time" in df.columns:

        df["timestamp"] = pd.to_datetime(
            df["time"]
        )


    # индикаторы

    df["EMA20"] = (
        df["close"]
        .ewm(span=20)
        .mean()
    )

    df["EMA50"] = (
        df["close"]
        .ewm(span=50)
        .mean()
    )

    df["EMA200"] = (
        df["close"]
        .ewm(span=200)
        .mean()
    )


    folder = Path("charts")

    folder.mkdir(
        exist_ok=True
    )


    filename = (
        symbol.replace("/", "_")
        +
        "_"
        +
        timeframe
        +
        ".png"
    )


    path = folder / filename



    fig, (ax, ax_volume) = plt.subplots(

        2,

        1,

        figsize=(14,8),

        gridspec_kw={
            "height_ratios":[3,1]
        },

        sharex=True

    )



    # свечи

    for _, row in df.iterrows():


        color = (

            "green"

            if row.close >= row.open

            else "red"

        )


        ax.plot(

            [
                row.timestamp,
                row.timestamp
            ],

            [
                row.low,
                row.high
            ],

            color=color

        )


        ax.bar(

            row.timestamp,

            row.close - row.open,

            bottom=row.open,

            width=0.005,

            color=color

        )



    # EMA

    ax.plot(

        df.timestamp,

        df.EMA20,

        label="EMA20"

    )


    ax.plot(

        df.timestamp,

        df.EMA50,

        label="EMA50"

    )


    ax.plot(

        df.timestamp,

        df.EMA200,

        label="EMA200"

    )



    ax.set_title(

        f"{symbol} {timeframe}"

    )


    ax.legend()



    # объём

    ax_volume.bar(

        df.timestamp,

        df.volume

    )



    ax.xaxis.set_major_formatter(

        mdates.DateFormatter(
            "%H:%M"
        )

    )


    plt.tight_layout()


    plt.savefig(

        path,

        dpi=200

    )


    plt.close()


    return str(path)
