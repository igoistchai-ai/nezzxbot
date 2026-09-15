import ccxt
import pandas as pd
from config import settings

_exchange = ccxt.okx({
    "enableRateLimit": True,
    "options": {"defaultType": "spot"},
})

def _normalize(symbol: str) -> str:
    symbol = symbol.strip().upper().replace("-", "/").replace("_", "/")
    if "/" not in symbol and symbol.endswith("USDT"):
        symbol = symbol[:-4] + "/USDT"
    return symbol

def validate_symbol(symbol: str) -> str:
    symbol = _normalize(symbol)
    markets = _exchange.load_markets()
    if symbol not in markets:
        raise ValueError(f"Пара {symbol} недоступна на OKX")
    if not markets[symbol].get("spot", False):
        raise ValueError(f"Пара {symbol} не является спотовой парой OKX")
    return symbol

def candles(symbol: str, timeframe="15m", limit=None) -> pd.DataFrame:
    symbol = validate_symbol(symbol)
    limit = max(50, min(int(limit or settings.candle_limit), 1000))
    rows = _exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    if not rows:
        raise RuntimeError("Биржа не вернула свечи.")
    df = pd.DataFrame(rows, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    valid = (
        (df.high >= df[["open","close"]].max(axis=1)) &
        (df.low <= df[["open","close"]].min(axis=1)) &
        (df.high >= df.low) & (df.volume >= 0)
    )
    df = df.loc[valid].reset_index(drop=True)
    if len(df) < 20:
        raise RuntimeError("Недостаточно корректных свечей.")
    return df

def ticker(symbol: str) -> dict:
    symbol = validate_symbol(symbol)
    t = _exchange.fetch_ticker(symbol)
    return {
        "symbol": symbol,
        "last": float(t["last"]),
        "bid": float(t["bid"]) if t.get("bid") is not None else None,
        "ask": float(t["ask"]) if t.get("ask") is not None else None,
        "volume": float(t["baseVolume"]) if t.get("baseVolume") is not None else None,
        "timestamp": t.get("timestamp"),
        "datetime": t.get("datetime"),
        "source": "OKX",
    }

def market_snapshot(symbol: str, timeframe="15m", limit=None) -> dict:
    df = candles(symbol, timeframe, limit)
    t = ticker(symbol)
    return {
        "source": "OKX",
        "symbol": symbol,
        "timeframe": timeframe,
        "ticker": t,
        "candles": [
            {
                "timestamp": int(r.timestamp().timestamp()*1000),
                "open": float(o), "high": float(h), "low": float(l),
                "close": float(c), "volume": float(v)
            }
            for r,o,h,l,c,v in zip(
                df["timestamp"], df["open"], df["high"], df["low"], df["close"], df["volume"]
            )
        ],
    }
