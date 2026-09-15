import time
import ccxt
import pandas as pd


exchange = ccxt.okx({
    "enableRateLimit": True,
})


CACHE = {}

CACHE_TIME = 2



def normalize(symbol):

    symbol = symbol.upper()

    if "/" not in symbol:
        symbol += "/USDT"

    return symbol



def get_candles(
        symbol,
        timeframe="15m",
        limit=120
):

    symbol = normalize(symbol)

    key = f"{symbol}_{timeframe}_{limit}"


    now = time.time()


    if key in CACHE:

        if now - CACHE[key]["time"] < CACHE_TIME:
            return CACHE[key]["data"]



    data = exchange.fetch_ohlcv(

        symbol,

        timeframe=timeframe,

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


    CACHE[key] = {

        "time": now,

        "data": df

    }


    return df




def get_price(symbol):

    symbol = normalize(symbol)


    ticker = exchange.fetch_ticker(
        symbol
    )


    return float(
        ticker["last"]
    )




def get_market_data(
        symbol,
        timeframe="15m"
):


    df = get_candles(

        symbol,

        timeframe,

        120

    )


    last = df.iloc[-1]


    return {

        "symbol": normalize(symbol),

        "price": float(last.close),

        "candles": [

            {

                "time": str(row.timestamp),

                "open": float(row.open),

                "high": float(row.high),

                "low": float(row.low),

                "close": float(row.close),

                "volume": float(row.volume)

            }

            for _, row in df.tail(50).iterrows()

        ]

    }
