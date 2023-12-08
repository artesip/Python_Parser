import sys
import asyncio
import logging
from Handlers import dp, bot


async def start(dp, bot):
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(start(dp, bot))
    except KeyboardInterrupt:
        print("Pressed Ctrl + smth")
