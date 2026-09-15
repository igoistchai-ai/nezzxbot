import mplfinance as mpf
from pathlib import Path
import pandas as pd


def create_chart(df, symbol, timeframe="15m"):
    df = df.copy()

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    elif "time" in df.columns:
        df["timestamp"] = pd.to_datetime(df["time"])

    df = df.set_index("timestamp")

    folder = Path("charts")
    folder.mkdir(exist_ok=True)

    file = folder / f"{symbol.replace('/','_')}_{timeframe}.png"

    style = mpf.make_mpf_style(
        base_mpf_style="charles"
    )

    add = [
        mpf.make_addplot(
            df["EMA20"],
            color="blue"
        ),
        mpf.make_addplot(
            df["EMA50"],
            color="orange"
        )
    ]

    mpf.plot(
        df,
        type="candle",
        volume=True,
        addplot=add,
        style=style,
        title=f"{symbol} {timeframe}",
        savefig=str(file),
        figsize=(12,7)
    )

    return str(file)
