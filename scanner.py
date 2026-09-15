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


    delta=df.close.diff()


    gain=(
        delta
        .clip(lower=0)
        .rolling(14)
        .mean()
    )


    loss=(
        -delta
        .clip(upper=0)
        .rolling(14)
        .mean()
    )


    rs=gain/loss


    rsi=100-(100/(1+rs))


    last=df.iloc[-1]


    return {


        "price":
        round(float(last.close),4),


        "trend":

        "BULLISH"

        if last.EMA20 > last.EMA50

        else "BEARISH",



        "EMA20":
        round(float(last.EMA20),4),



        "EMA50":
        round(float(last.EMA50),4),



        "RSI":
        round(float(rsi.iloc[-1]),2),



        "volume":
        round(float(last.volume),2)

    }
