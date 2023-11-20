from setings.config import GLOBAL_LINK, SEARCH, PRICE, ITER_LINK
from core.bot_servise import BotService
from utilities.variables import Product, ConfigSettings, RequestConfig,Cards

from os import path

from db.dbmanager import DBManager
from loguru import logger
from time import sleep


class Parser(BotService):
    def __init__(self):
        super().__init__()
        self.config = ConfigSettings(GLOBAL_LINK, ITER_LINK)
        self.product = Product(SEARCH, PRICE)

    def run(self):
        link = self.config.create_link(self.product)
        soup = RequestConfig().start(link)
        div = soup.find_all('div', attrs={'data-cy': 'l-card'})
        s=Cards(self.db).search_cards(soup,self.product.search)

        if soup:
            sleep(15)
            self.run()
