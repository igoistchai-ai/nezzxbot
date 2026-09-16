from aiohttp import web
import asyncio
import os



async def health(request):

    return web.Response(
        text="NEZZX AI is alive"
    )





async def start_health():

    app = web.Application()


    app.router.add_get(
        "/",
        health
    )


    app.router.add_get(
        "/health",
        health
    )


    runner = web.AppRunner(
        app
    )


    await runner.setup()



    port = int(
        os.getenv(
            "PORT",
            4000
        )
    )



    site = web.TCPSite(

        runner,

        "0.0.0.0",

        port

    )


    await site.start()



    print(
        f"Health server started on {port}"
    )
