from setings.config import GLOBAL_LINK, SEARCH, PRICE, ITER_LINK
from core.bot_servise import BotService
from utilities.variables_class import Product, ConfigSettings, RequestConfig
from core.cards import Cards
from schedule import every, repeat, run_pending
from datetime import datetime as dt
from os import path

from db.dbmanager import DBManager
from loguru import logger
from time import sleep


class Parser(BotService):
    def __init__(self):
        super().__init__()
        self.config = ConfigSettings(GLOBAL_LINK, ITER_LINK)
        self.product = Product(SEARCH, PRICE)

    def search_count_pages(self, soup):
        try:
            cards = soup.find('ul', class_="pagination-list").find_all('li')
            page_number = cards[-1].find('a').text
            return int(page_number)
        except Exception as e:
            return 1


    def start(self):
        @repeat(every(1).minutes)
        def run():
            current_time = dt.now().time()
            logger.info(current_time)
            if current_time.hour >= 9 and current_time.hour < 21:

                link = self.config.create_link(self.product)
                soup = RequestConfig().start(link)

                for i in range(1, self.search_count_pages(soup) + 1):
                    if i == 1:
                        Cards(self.db).search_cards(soup, self.product.search)
                    else:
                        link = self.config.create_link_page(self.product, i)
                        soup = RequestConfig().start(link)
                        Cards(self.db).search_cards(soup, self.product.search)

        while True:
            run_pending()
            sleep(1)
