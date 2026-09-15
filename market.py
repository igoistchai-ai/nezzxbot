import ccxt
import pandas as pd

from config import settings



exchange = ccxt.okx({

    "enableRateLimit": True,

    "options":{
        "defaultType":"spot"
    }

})



def normalize(symbol):

    symbol = symbol.upper()


    if "/" not in symbol:

        symbol += "/USDT"


    return symbol




def candles(
        symbol,
        timeframe="15m",
        limit=None
):


    symbol = normalize(symbol)


    data = exchange.fetch_ohlcv(

        symbol,

        timeframe,

        limit=limit or settings.candle_limit

    )


    df = pd.DataFrame(

        data,

        columns=[

            "timestamp",

            "open",

            "high",

            "low",

            "close",

            "volume"

        ]

    )


    df["timestamp"] = pd.to_datetime(

        df["timestamp"],

        unit="ms"

    )


    return df




def market_snapshot(
        symbol,
        timeframe="15m"
):


    df = candles(

        symbol,

        timeframe

    )


    return {


        "symbol":
            normalize(symbol),


        "timeframe":
            timeframe,


        "price":
            float(
                df.iloc[-1].close
            ),


        "candles":[


            {

                "time":
                    str(row.timestamp),

                "open":
                    float(row.open),

                "high":
                    float(row.high),

                "low":
                    float(row.low),

                "close":
                    float(row.close),

                "volume":
                    float(row.volume)

            }


            for _,row in df.iterrows()

        ]

    }
