from fake_useragent import UserAgent
from requests import session
from bs4 import BeautifulSoup
from loguru import logger
from db.table.product_card import ProductCard as card_table
from datetime import datetime as dt
from utilities.web_draver import WebDriverClient


class Product:
    def __init__(self, search, price):
        self.search = search
        self.price_st = str(price[0])
        self.price_end = str(price[1])


class ConfigSettings:
    def __init__(self, link, iter_link):
        self.link_global = link
        self.keywords = iter_link[0]
        self.price_st = iter_link[1]
        self.price_end = iter_link[2]
        self.page = iter_link[3]
        self.page_price_st=iter_link[4]
        self.page_price_end = iter_link[5]
        self.link = None

    def create_link(self, product):

        # self.link = self.link_global + self.keywords
        # keywords_link = None
        # for item in product.search:
        #     if keywords_link:
        #         keywords_link = keywords_link + "-" + item
        #     else:
        #         keywords_link = item
        #
        # keywords_link = keywords_link + '/'
        # self.link = self.link + keywords_link + self.price_st + product.price_st + self.price_end + product.price_end
        # return self.link

        self.link = f"{self.link_global}{self.keywords}"

        keywords_link = '-'.join(product.search) + '/' if product.search else ''
        price_segment = f"{self.price_st}{product.price_st}{self.price_end}{product.price_end}"

        self.link = f"{self.link}{keywords_link}{price_segment}"
        return self.link

    def create_link_page(self, product, number_page):
        # self.link = self.link_global + self.keywords
        # keywords_link = None
        # for item in product.search:
        #     if keywords_link:
        #         keywords_link = keywords_link + "-" + item
        #     else:
        #         keywords_link = item
        #
        # keywords_link = keywords_link + '/'
        # self.link = self.link + keywords_link + self.page + str(number_page) + self.page_price_st + product.price_st + self.page_price_end + product.price_end
        # return self.link

        self.link = self.link_global + self.keywords
        keywords_link = "-".join(product.search) + '/' if product.search else ''
        self.link = f"{self.link}{keywords_link}{self.page}{number_page}{self.page_price_st}{product.price_st}{self.page_price_end}{product.price_end}"
        return self.link


class RequestConfig:
    def __init__(self):
        self.request = WebDriverClient()

        self.user_agent = UserAgent().random
        self.headers = {"user-agent": self.user_agent}

    def get_html(self, link):
        html = self.request.get_response(link)
        self.request.dispose()
        return html[0]
        # if respons.status_code == 200:
        #     return respons.text
        # else:
        #     logger.error(f"Respons code: {respons.status_code}")

    def get_soup(self, html):
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def start(self, link):
        soup = self.get_html(link)
        if soup:
            return self.get_soup(soup)
