import asyncio

from bot import main
from health_server import start_health


async def start():
    # Render provides the HTTP port through the PORT environment variable.
    # The health server uses that same port so UptimeRobot can ping /health.
    await start_health()

    # Start Telegram polling in the same process.
    await main()


if __name__ == "__main__":
    asyncio.run(start())
