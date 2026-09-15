import mplfinance as mpf
import pandas as pd
from pathlib import Path


def render_chart(
        df,
        symbol,
        timeframe="15m",
        signal=None
):

    data = df.copy()


    if "timestamp" in data.columns:

        data["timestamp"] = pd.to_datetime(
            data["timestamp"]
        )

        data = data.set_index(
            "timestamp"
        )


    data = data.rename(
        columns={
            "open":"Open",
            "high":"High",
            "low":"Low",
            "close":"Close",
            "volume":"Volume"
        }
    )


    # EMA

    data["EMA20"] = (
        data["Close"]
        .ewm(span=20)
        .mean()
    )


    data["EMA50"] = (
        data["Close"]
        .ewm(span=50)
        .mean()
    )


    addplots = [

        mpf.make_addplot(
            data["EMA20"],
            color="blue"
        ),

        mpf.make_addplot(
            data["EMA50"],
            color="orange"
        )

    ]


    # уровни AI

    if signal:

        if "entry" in signal:

            entry = float(
                signal["entry"]
            )

            data["ENTRY"] = entry


            addplots.append(

                mpf.make_addplot(

                    data["ENTRY"],

                    color="green",

                    linestyle="--"

                )

            )


        if "stop" in signal:

            stop = float(
                signal["stop"]
            )

            data["STOP"] = stop


            addplots.append(

                mpf.make_addplot(

                    data["STOP"],

                    color="red",

                    linestyle="--"

                )

            )



    folder = Path("charts")

    folder.mkdir(
        exist_ok=True
    )


    filename = (

        symbol.replace("/","_")

        +

        "_"

        +

        timeframe

        +

        ".png"

    )


    path = folder / filename



    mpf.plot(

        data.tail(100),

        type="candle",

        style="charles",

        volume=True,

        addplot=addplots,

        title=f"{symbol} {timeframe}",

        figsize=(14,8),

        savefig=str(path)

    )


    return str(path)
