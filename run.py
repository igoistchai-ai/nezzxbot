import asyncio


from bot import main, bot


from health_server import start_health


from price_monitor import monitor_prices





async def start():


    # запуск страницы для Render/UptimeRobot

    await start_health()



    # запуск мониторинга цен

    asyncio.create_task(

        monitor_prices(bot)

    )



    # запуск Telegram

    await main()





if __name__ == "__main__":


    asyncio.run(
        start()
    )
