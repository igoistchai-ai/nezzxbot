import asyncio
import json
import websockets


async def watch_price(symbol, callback):

    pair=symbol.replace("/","-").lower()

    url="wss://ws.okx.com:8443/ws/v5/public"

    async with websockets.connect(url) as ws:

        await ws.send(json.dumps({
            "op":"subscribe",
            "args":[
                {
                    "channel":"tickers",
                    "instId":pair.upper()
                }
            ]
        }))

        async for msg in ws:
            data=json.loads(msg)

            if "data" in data:
                price=data["data"][0]["last"]
                await callback(symbol,float(price))
