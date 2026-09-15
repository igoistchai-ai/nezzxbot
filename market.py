import time

import ccxt

import pandas as pd



exchange = ccxt.okx({

    "enableRateLimit": True

})



CACHE = {}

CACHE_TIME = 3





def normalize(symbol):


    symbol=symbol.upper()


    if "/" not in symbol:

        symbol += "/USDT"


    return symbol





def get_candles(

        symbol,

        timeframe="15m",

        limit=120

):


    symbol=normalize(symbol)


    key=f"{symbol}_{timeframe}"



    now=time.time()



    if key in CACHE:


        if now-CACHE[key]["time"] < CACHE_TIME:

            return CACHE[key]["data"]




    data=exchange.fetch_ohlcv(

        symbol,

        timeframe,

        limit=limit

    )



    df=pd.DataFrame(

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



    df["timestamp"]=pd.to_datetime(

        df["timestamp"],

        unit="ms"

    )



    CACHE[key]={

        "time":now,

        "data":df

    }



    return df






def get_market_snapshot(symbol):


    df=get_candles(

        symbol

    )



    last=df.iloc[-1]



    return {


        "symbol":normalize(symbol),


        "price":float(last.close),


        "candles":[


            {

                "open":float(row.open),

                "high":float(row.high),

                "low":float(row.low),

                "close":float(row.close),

                "volume":float(row.volume)

            }


            for _,row in df.tail(50).iterrows()

        ]

    }
