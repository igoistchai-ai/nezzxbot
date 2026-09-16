import aiohttp
import time

CACHE = {}
CACHE_TIME = 2


async def get_candles(symbol="BTC-USDT", limit=100):
    global CACHE

    now = time.time()

    key = f"{symbol}_{limit}"

    if key in CACHE:
        if now - CACHE[key]["time"] < CACHE_TIME:
            return CACHE[key]["data"]

    url = "https://www.okx.com/api/v5/market/candles"

    params = {
        "instId": symbol,
        "bar": "1m",
        "limit": str(limit)
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                timeout=5
            ) as r:

                data = await r.json()

                candles = []

                for c in reversed(data["data"]):
                    candles.append({
                        "time": c[0],
                        "open": float(c[1]),
                        "high": float(c[2]),
                        "low": float(c[3]),
                        "close": float(c[4]),
                        "volume": float(c[5])
                    })


                CACHE[key] = {
                    "time": now,
                    "data": candles
                }

                return candles


    except Exception as e:
        print("MARKET ERROR:", e)
        return []
