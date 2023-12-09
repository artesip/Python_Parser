import sys
import asyncio
import logging
from Handlers import dp, bot, site_parse_with_announcement

async def update_db():
    while True:
        await asyncio.sleep(60 * 60 * 24)
        await site_parse_with_announcement()


async def start(dp, bot):
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    loop = asyncio.get_event_loop()
    
    loop.create_task(update_db())
    
    try:
        loop.run_until_complete(start(dp, bot))
    except KeyboardInterrupt:
        print("Pressed Ctrl + smth")
    finally:
        loop.close()
