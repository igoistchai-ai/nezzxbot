import mplfinance as mpf
from pathlib import Path


def create_chart(df, symbol, timeframe="15m"):

    data = df.copy()


    # берём только последние свечи
    data = data.tail(100).copy()


    data["EMA20"] = (
        data["close"]
        .ewm(span=20)
        .mean()
    )


    data["EMA50"] = (
        data["close"]
        .ewm(span=50)
        .mean()
    )


    data = data.rename(
        columns={
            "timestamp":"Date",
            "open":"Open",
            "high":"High",
            "low":"Low",
            "close":"Close",
            "volume":"Volume"
        }
    )


    data["Date"] = data["Date"].astype(
        "datetime64[ns]"
    )


    data = data.set_index(
        "Date"
    )


    folder = Path("charts")
    folder.mkdir(
        exist_ok=True
    )


    path = folder / (
        symbol.replace("/", "_")
        +
        "_"
        +
        timeframe
        +
        ".png"
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


    mpf.plot(

        data,

        type="candle",

        style="charles",

        volume=True,

        addplot=addplots,

        title=f"{symbol} {timeframe}",

        savefig={
            "fname":str(path),
            "dpi":120,
            "bbox_inches":"tight"
        }

    )


    return str(path)
