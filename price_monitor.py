import asyncio
import json
import websockets


from alerts import check_price



SYMBOLS = [

    "BTC-USDT",
    "ETH-USDT",
    "LTC-USDT",
    "SOL-USDT"

]



async def monitor_prices(bot):


    url = (
        "wss://ws.okx.com:8443/ws/v5/public"
    )


    while True:

        try:

            async with websockets.connect(
                url,
                ping_interval=20,
                ping_timeout=20
            ) as ws:


                await ws.send(
                    json.dumps({

                        "op": "subscribe",

                        "args": [

                            {

                                "channel": "tickers",

                                "instId": symbol

                            }

                            for symbol in SYMBOLS

                        ]

                    })
                )


                print(
                    "✅ Price monitor started"
                )



                while True:


                    msg = await ws.recv()


                    data = json.loads(
                        msg
                    )


                    if "data" not in data:

                        continue



                    prices = {}



                    for item in data["data"]:


                        symbol = (

                            item["instId"]

                            .replace(
                                "-",
                                "/"
                            )

                        )


                        prices[symbol] = float(

                            item["last"]

                        )



                    triggered = check_price(
                        prices
                    )



                    for alert in triggered:


                        await bot.send_message(

                            chat_id=int(
                                alert["user"]
                            ),

                            text=(

                                "🚨 ЦЕНА ДОСТИГНУТА\n\n"

                                f"🪙 {alert['symbol']}\n"

                                f"💰 Цена: {alert['price']}"

                            )

                        )



                    await asyncio.sleep(
                        0.5
                    )



        except Exception as e:


            print(
                "Price monitor error:",
                e
            )


            await asyncio.sleep(
                5
            )
