import mplfinance as mpf
from pathlib import Path



def create_chart(
        df,
        symbol,
        timeframe="15m"
):


    data=df.copy()


    data["EMA20"] = (
        data.close
        .ewm(span=20)
        .mean()
    )


    data["EMA50"] = (
        data.close
        .ewm(span=50)
        .mean()
    )



    data=data.rename(

        columns={

            "timestamp":"Date",

            "open":"Open",

            "high":"High",

            "low":"Low",

            "close":"Close",

            "volume":"Volume"

        }

    )


    if "Date" in data:

        data=data.set_index(
            "Date"
        )



    folder=Path(
        "charts"
    )

    folder.mkdir(
        exist_ok=True
    )


    path=folder / (
        symbol.replace("/","_")
        +
        "_"
        +
        timeframe
        +
        ".png"
    )



    plots=[

        mpf.make_addplot(

            data["EMA20"],

            color="blue"

        ),

        mpf.make_addplot(

            data["EMA50"],

            color="orange"

        )

    ]



    mpf.plot(

        data.tail(100),

        type="candle",

        volume=True,

        style="charles",

        addplot=plots,

        title=f"{symbol} {timeframe}",

        savefig=str(path),

        figsize=(14,8)

    )


    return str(path)
