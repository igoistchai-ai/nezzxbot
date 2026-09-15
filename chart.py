import mplfinance as mpf
import pandas as pd
from pathlib import Path



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


    data = data.tail(100)


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


    data = data.set_index(
        "Date"
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



    hlines = []



    if analysis:


        # вход

        if "entry" in analysis:


            hlines.append(

                float(
                    analysis["entry"]
                )

            )



        # стоп

        if "sl" in analysis:


            hlines.append(

                float(
                    analysis["sl"]
                )

            )



        # тейк

        if "tp" in analysis:


            hlines.append(

                float(
                    analysis["tp"]
                )

            )





    folder = Path(
        "charts"
    )

    folder.mkdir(
        exist_ok=True
    )



    file = folder / (

        symbol.replace("/","_")

        +

        "_chart.png"

    )



    mpf.plot(

        data,

        type="candle",

        style="charles",

        volume=True,


        addplot=addplots,


        hlines={

            "hlines":hlines,

            "colors":[

                "green",

                "red",

                "green"

            ],

            "linestyle":"--"

        } if hlines else None,


        title=f"{symbol} {timeframe}",


        figsize=(14,8),


        savefig={

            "fname":str(file),

            "dpi":120

        }

    )



    return str(file)
