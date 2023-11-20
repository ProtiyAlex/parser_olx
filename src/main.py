import os
import sys
from loguru import logger




from core.parser import Parser

if __name__ == '__main__':
    try:

        bot = Parser()
        bot.start()

    except Exception as e:
        logger.error(f"Reload Bot Parser. Error {e}")
        # telegram_bot_sendtext(f"Reload Bot Parser. Error {e}")
        # os.execl(sys.executable, sys.executable, *sys.argv)
