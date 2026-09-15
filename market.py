import ccxt
import pandas as pd

from config import settings



exchange = ccxt.okx({

    "enableRateLimit": True,

    "options": {

        "defaultType": settings.market_type

    }

})



def normalize_symbol(symbol):

    symbol = symbol.upper()


    if "/" not in symbol:

        symbol = symbol + "/USDT"


    return symbol





def candles(
        symbol,
        timeframe="15m"
):

    symbol = normalize_symbol(symbol)


    data = exchange.fetch_ohlcv(

        symbol,

        timeframe=timeframe,

        limit=settings.candle_limit

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


    last = df.iloc[-1]



    return {


        "symbol":

            normalize_symbol(symbol),



        "timeframe":

            timeframe,



        "price":

            float(last.close),



        "candles": [


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


            for _, row in df.iterrows()

        ]

    }
