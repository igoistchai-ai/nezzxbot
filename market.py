import ccxt
import pandas as pd

from config import settings


exchange = ccxt.okx({
    "enableRateLimit": True,
    "options": {
        "defaultType": "spot"
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
        limit=100
):

    symbol = normalize(symbol)


    data = exchange.fetch_ohlcv(

        symbol,

        timeframe,

        limit=limit

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
        timeframe,
        100
    )


    last = df.iloc[-1]


    return {

        "symbol": normalize(symbol),

        "price": round(
            float(last.close),
            4
        ),

        "candles": [

            {

            "open":float(x.open),
            "high":float(x.high),
            "low":float(x.low),
            "close":float(x.close),
            "volume":float(x.volume)

            }

            for _,x in df.tail(20).iterrows()

        ]

    }
