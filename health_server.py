import os

from aiohttp import web


app = web.Application()


async def health(request):
    return web.json_response(
        {
            "status": "online",
            "service": "NEZZX GRAFIK AI",
        }
    )


app.router.add_get("/", health)
app.router.add_get("/health", health)


async def start_health():
    # Render automatically provides PORT.
    # Local fallback is 4000.
    port = int(os.getenv("PORT", "4000"))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port,
    )

    await site.start()

    print(f"Health server listening on 0.0.0.0:{port}")
