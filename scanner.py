import pandas as pd



def calculate_rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)


    avg_gain = gain.rolling(
        period
    ).mean()


    avg_loss = loss.rolling(
        period
    ).mean()


    rs = avg_gain / avg_loss


    return 100 - (
        100/(1+rs)
    )





def scan(df):


    df=df.copy()


    df["EMA20"] = (
        df.close
        .ewm(span=20)
        .mean()
    )


    df["EMA50"] = (
        df.close
        .ewm(span=50)
        .mean()
    )


    df["RSI"] = calculate_rsi(
        df.close
    )


    last=df.iloc[-1]


    price=float(
        last.close
    )


    if last.EMA20 > last.EMA50:

        signal="LONG"

        entry=price

        tp=price*1.02

        sl=price*0.99


    else:

        signal="SHORT"

        entry=price

        tp=price*0.98

        sl=price*1.01




    return {


        "price":round(price,6),

        "signal":signal,

        "entry":round(entry,6),

        "tp":round(tp,6),

        "sl":round(sl,6),


        "rsi":round(
            float(last.RSI),
            2
        ),


        "ema20":round(
            float(last.EMA20),
            6
        ),


        "ema50":round(
            float(last.EMA50),
            6
        ),


        "volume":float(
            last.volume
        )

    }
