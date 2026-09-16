import mplfinance as mpf
from pathlib import Path
import pandas as pd



def create_chart(
        df,
        symbol,
        analysis=None,
        timeframe="15m"
):

    data = df.copy()


    data["timestamp"] = pd.to_datetime(
        data["timestamp"]
    )


    data = data.tail(80)


    data = data.rename(
        columns={

            "timestamp": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"

        }
    )


    data = data.set_index(
        "Date"
    )



    # EMA

    data["EMA20"] = (
        data["Close"]
        .ewm(
            span=20,
            adjust=False
        )
        .mean()
    )


    data["EMA50"] = (
        data["Close"]
        .ewm(
            span=50,
            adjust=False
        )
        .mean()
    )



    plots = [

        mpf.make_addplot(
            data["EMA20"]
        ),

        mpf.make_addplot(
            data["EMA50"]
        )

    ]



    levels = []


    colors = []



    if analysis:


        if analysis.get("entry"):

            levels.append(
                analysis["entry"]
            )

            colors.append(
                "green"
            )



        if analysis.get("tp1"):

            levels.append(
                analysis["tp1"]
            )

            colors.append(
                "green"
            )



        if analysis.get("tp2"):

            levels.append(
                analysis["tp2"]
            )

            colors.append(
                "green"
            )



        if analysis.get("sl"):

            levels.append(
                analysis["sl"]
            )

            colors.append(
                "red"
            )



    Path(
        "charts"
    ).mkdir(
        exist_ok=True
    )



    file = (

        "charts/"

        +

        symbol.replace(
            "/",
            "_"
        )

        +

        ".png"

    )



    mpf.plot(

        data,

        type="candle",

        style="charles",

        volume=True,


        addplot=plots,


        hlines={

            "hlines": levels,

            "colors": colors,

            "linestyle": "--",

            "linewidths": 1.2

        } if levels else None,


        title=f"{symbol} {timeframe}",


        figsize=(14,8),


        savefig={

            "fname": file,

            "dpi":120,

            "bbox_inches":"tight"

        }

    )


    return file
