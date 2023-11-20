
from loguru import logger

from setings.config import FILENAME_LOG



from time import sleep
from db.dbmanager import DBManager


class BotService:
    def __init__(self):
        self.init_loguru()
        self.db = DBManager()


    def init_loguru(self):
        logger.add(FILENAME_LOG, format="{time} {level} {message}",
                   level="INFO", rotation="10 MB", compression="zip")
        logger.info("Bot запускается...")




