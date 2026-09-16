import pandas as pd



def calculate_rsi(series, period=14):

    delta = series.diff()


    gain = delta.clip(
        lower=0
    )


    loss = -delta.clip(
        upper=0
    )


    avg_gain = gain.rolling(
        period
    ).mean()


    avg_loss = loss.rolling(
        period
    ).mean()


    rs = avg_gain / avg_loss


    rsi = 100 - (
        100 / (1 + rs)
    )


    return rsi





def prepare_indicators(df):

    df = df.copy()


    df["EMA20"] = (
        df["close"]
        .ewm(
            span=20,
            adjust=False
        )
        .mean()
    )


    df["EMA50"] = (
        df["close"]
        .ewm(
            span=50,
            adjust=False
        )
        .mean()
    )


    df["RSI"] = calculate_rsi(
        df["close"]
    )


    return df





def scan(df, symbol=""):

    df = prepare_indicators(
        df
    )


    last = df.iloc[-1]


    price = float(
        last["close"]
    )


    ema20 = float(
        last["EMA20"]
    )


    ema50 = float(
        last["EMA50"]
    )


    rsi = float(
        last["RSI"]
    )



    # Логика сигнала


    if (
        ema20 > ema50
        and rsi < 70
    ):

        signal = "LONG"


        entry = price


        tp1 = price * 1.01


        tp2 = price * 1.02


        sl = price * 0.985



    elif (
        ema20 < ema50
        and rsi > 30
    ):

        signal = "SHORT"


        entry = price


        tp1 = price * 0.99


        tp2 = price * 0.98


        sl = price * 1.015



    else:


        signal = "WAIT"


        entry = price


        tp1 = price


        tp2 = price


        sl = price





    return {

        "symbol": symbol,


        "price": round(
            price,
            8
        ),


        "signal": signal,


        "entry": round(
            entry,
            8
        ),


        "tp1": round(
            tp1,
            8
        ),


        "tp2": round(
            tp2,
            8
        ),


        "sl": round(
            sl,
            8
        ),


        "rsi": round(
            rsi,
            2
        ),


        "ema20": round(
            ema20,
            8
        ),


        "ema50": round(
            ema50,
            8
        )

        }
