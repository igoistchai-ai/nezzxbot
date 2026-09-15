import pandas as pd


def scan(df):
    df=df.copy()

    df["EMA20"]=df.close.ewm(span=20).mean()
    df["EMA50"]=df.close.ewm(span=50).mean()

    delta=df.close.diff()
    gain=delta.clip(lower=0).rolling(14).mean()
    loss=-delta.clip(upper=0).rolling(14).mean()

    rs=gain/loss
    df["RSI"]=100-(100/(1+rs))

    last=df.iloc[-1]

    return {
        "price":float(last.close),
        "ema20":float(last.EMA20),
        "ema50":float(last.EMA50),
        "rsi":float(last.RSI),
        "trend":"LONG" if last.EMA20>last.EMA50 else "SHORT"
    }
