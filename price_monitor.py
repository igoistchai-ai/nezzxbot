import asyncio
import json
import websockets


from alerts import check_price



async def monitor_prices(bot):


    url = (
        "wss://ws.okx.com:8443/ws/v5/public"
    )


    symbols = [

        "BTC-USDT",
        "ETH-USDT",
        "LTC-USDT",
        "SOL-USDT",
        "DOGE-USDT"

    ]



    while True:


        try:


            async with websockets.connect(
                url
            ) as ws:



                await ws.send(

                    json.dumps({

                        "op":"subscribe",

                        "args":[

                            {

                                "channel":"tickers",

                                "instId":symbol

                            }

                            for symbol in symbols

                        ]

                    })

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



                    alerts = check_price(
                        prices
                    )



                    for alert in alerts:


                        await bot.send_message(

                            chat_id=int(
                                alert["user"]
                            ),


                            text=f"""

🚨 Цена достигнута!


🪙 Монета:
{alert['symbol']}


💰 Цена:
{alert['price']}


"""

                        )



                    await asyncio.sleep(
                        0.5
                    )



        except Exception as e:


            print(
                "WebSocket error:",
                e
            )


            await asyncio.sleep(
                5
            )
