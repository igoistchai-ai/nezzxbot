import asyncio


from bot import main, bot

from price_monitor import monitor_prices

from health_server import start_health





async def start():


    # Render / UptimeRobot

    await start_health()



    # уведомления цены

    asyncio.create_task(

        monitor_prices(bot)

    )



    # Telegram

    await main()





if __name__ == "__main__":

    asyncio.run(
        start()
    )
