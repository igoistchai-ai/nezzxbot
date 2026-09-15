import math
import pandas as pd

def _ema(s, n):
    return s.ewm(span=n, adjust=False).mean()

def _rsi(s, n=14):
    d = s.diff()
    gain = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    loss = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = gain / loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))

def _atr(df, n=14):
    prev = df.close.shift(1)
    tr = pd.concat([
        df.high-df.low, (df.high-prev).abs(), (df.low-prev).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(alpha=1/n, adjust=False).mean()

def enrich(df):
    x = df.copy()
    x["ema20"] = _ema(x.close, 20)
    x["ema50"] = _ema(x.close, 50)
    x["ema200"] = _ema(x.close, 200)
    x["rsi14"] = _rsi(x.close)
    x["atr14"] = _atr(x)
    x["vol_ma20"] = x.volume.rolling(20).mean()
    return x

def scan(df):
    x = enrich(df)
    r = x.iloc[-1]
    recent = x.tail(30)
    trend = "UP" if r.ema20 > r.ema50 else "DOWN"
    if abs(r.ema20-r.ema50) / max(r.close, 1) < 0.002:
        trend = "RANGE"

    swing_high = float(recent.high.max())
    swing_low = float(recent.low.min())
    volume_ratio = float(r.volume / r.vol_ma20) if r.vol_ma20 else None

    candle_body = abs(r.close-r.open)
    candle_range = max(r.high-r.low, 1e-12)
    upper = r.high-max(r.open,r.close)
    lower = min(r.open,r.close)-r.low

    candle = "NONE"
    if candle_body/candle_range < 0.12:
        candle = "DOJI"
    elif lower > candle_body*2 and upper < candle_body:
        candle = "HAMMER"
    elif upper > candle_body*2 and lower < candle_body:
        candle = "SHOOTING_STAR"

    bullish = trend == "UP" and r.rsi14 < 70 and r.close >= r.ema20
    bearish = trend == "DOWN" and r.rsi14 > 30 and r.close <= r.ema20

    score_long = 0
    score_short = 0
    if trend == "UP": score_long += 25
    if trend == "DOWN": score_short += 25
    if r.close > r.ema20: score_long += 15
    if r.close < r.ema20: score_short += 15
    if 45 <= r.rsi14 <= 65: score_long += 10
    if 35 <= r.rsi14 <= 55: score_short += 10
    if volume_ratio and volume_ratio > 1.2:
        if r.close > r.open: score_long += 10
        if r.close < r.open: score_short += 10
    if candle in ("HAMMER",): score_long += 8
    if candle == "SHOOTING_STAR": score_short += 8

    return {
        "trend": trend,
        "price": float(r.close),
        "rsi14": float(r.rsi14),
        "atr14": float(r.atr14),
        "ema20": float(r.ema20),
        "ema50": float(r.ema50),
        "ema200": float(r.ema200) if not math.isnan(r.ema200) else None,
        "volume_ratio": volume_ratio,
        "recent_high": swing_high,
        "recent_low": swing_low,
        "candle": candle,
        "long_score": min(score_long, 100),
        "short_score": min(score_short, 100),
    }
