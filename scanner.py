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


    return 100 - (100/(1+rs))





def scan(df):


    data = df.copy()



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


    data["EMA200"] = (
        data["close"]
        .ewm(span=200)
        .mean()
    )



    data["RSI"] = calculate_rsi(
        data["close"]
    )



    last = data.iloc[-1]



    trend = "LONG"


    if last.EMA20 < last.EMA50:

        trend = "SHORT"



    support = (
        data["low"]
        .tail(50)
        .min()
    )


    resistance = (
        data["high"]
        .tail(50)
        .max()
    )



    return {


        "price":
            round(float(last.close),4),


        "trend":
            trend,


        "rsi":
            round(float(last.RSI),2),


        "ema20":
            round(float(last.EMA20),4),


        "ema50":
            round(float(last.EMA50),4),


        "ema200":
            round(float(last.EMA200),4),


        "support":
            round(float(support),4),


        "resistance":
            round(float(resistance),4),


        "volume":
            round(float(last.volume),2)

    }
