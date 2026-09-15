
import matplotlib.pyplot as plt
import matplotlib.dates as mpdates
from pathlib import Path
import pandas as pd


def create_chart(df, symbol, timeframe="15m"):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    out = Path("charts")
    out.mkdir(exist_ok=True)

    file = out / f"{symbol.replace('/','_')}_{timeframe}.png"

    df["ema20"] = df.close.ewm(span=20).mean()
    df["ema50"] = df.close.ewm(span=50).mean()
    df["ema200"] = df.close.ewm(span=200).mean()

    fig, (ax, vol) = plt.subplots(
        2, 1,
        figsize=(12, 8),
        sharex=True,
        gridspec_kw={"height_ratios":[3,1]}
    )

    for _, row in df.iterrows():
        color = "green" if row.close >= row.open else "red"

        ax.plot(
            [row.timestamp, row.timestamp],
            [row.low, row.high],
            color=color
        )

        ax.bar(
            row.timestamp,
            row.close-row.open,
            bottom=row.open,
            width=0.005,
            color=color
        )

    ax.plot(df.timestamp, df.ema20, label="EMA20")
    ax.plot(df.timestamp, df.ema50, label="EMA50")
    ax.plot(df.timestamp, df.ema200, label="EMA200")

    ax.set_title(f"{symbol} {timeframe}")
    ax.legend()

    vol.bar(df.timestamp, df.volume)

    ax.xaxis.set_major_formatter(
        mpdates.DateFormatter("%H:%M")
    )

    plt.tight_layout()
    plt.savefig(file, dpi=200)
    plt.close()

    return str(file)
