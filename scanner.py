import pandas as pd



def rsi_calc(series, period=14):

    delta = series.diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )


    avg_gain = gain.rolling(
        period
    ).mean()


    avg_loss = loss.rolling(
        period
    ).mean()


    rs = avg_gain / avg_loss


    return 100 - (
        100 / (1 + rs)
    )





def scan(df):


    data = df.copy()


    data["EMA20"] = (
        data.close
        .ewm(span=20)
        .mean()
    )


    data["EMA50"] = (
        data.close
        .ewm(span=50)
        .mean()
    )


    data["EMA200"] = (
        data.close
        .ewm(span=200)
        .mean()
    )


    data["RSI"] = rsi_calc(
        data.close
    )


    last = data.iloc[-1]


    if last.EMA20 > last.EMA50:

        trend = "LONG"

    else:

        trend = "SHORT"



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


        "volume":
        round(float(last.volume),2),


        "high":
        round(float(data.high.tail(50).max()),4),


        "low":
        round(float(data.low.tail(50).min()),4)

    }
