import sys
import time
import socket
import asyncio
import logging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
'''
while True:
    try:
        s.connect(('db', 5432))
        s.close
        break
    except socket.error as e:
        time.sleep(0.1)
'''
from Handlers import dp, bot


async def start(dp, bot):
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(start(dp, bot))
    except KeyboardInterrupt:
        print("Pressed Ctrl + smth")
