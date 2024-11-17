import asyncio
import logging
import sys

from src import bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(bot.main())
