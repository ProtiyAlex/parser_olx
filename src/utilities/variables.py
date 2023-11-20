from fake_useragent import UserAgent
from requests import session
from bs4 import BeautifulSoup
from loguru import logger
from db.table.product_card import ProductCard as card_table
from datetime import datetime as dt
from utilities.web_draver import WebDriverClient


class Cards:
    def __init__(self,db):
        self.attr = {'tag': 'div',
                     'attrs': {'data-cy': 'l-card'}}
        self.db=db

    def examination_title(self,title,search_title):
        # Преобразование всех слов в списке SEARCH к нижнему регистру
        search_lower = set(word.lower() for word in search_title)
        # Преобразование строки к нижнему регистру и разбиение на слова
        words_in_string = set(title.lower().split())
        # Проверка наличия всех слов из списка в строке
        all_words_present = all(word in words_in_string for word in search_lower)

        return all_words_present

    def search_cards(self, soup,search_title):
        cards = soup.find_all(self.attr['tag'], attrs=self.attr['attrs'])

        for soup_card in cards:
            card_t=card_table()
            card_t.img_link = soup_card.find('div', class_='css-gl6djm').find('img')['src']

            card_t.title = soup_card.find('h6').text
            card_t.price = soup_card.find('p', attrs={'data-testid': "ad-price"}).text
            card_t.location = soup_card.find('p', attrs={'data-testid': "location-date"}).text
            card_t.data = dt.now()
            card_t.link = soup_card.find('a', class_="css-rc5s2u").get('href')
            a = card_t
            if self.examination_title(card_t.title,search_title):
                self.db.add(card_t)
            # pass .strftime('%Y-%m-%d %H:%M')
        pass


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
        self.link = None

    def create_link(self, product):

        self.link = self.link_global + self.keywords
        keywords_link = None
        for item in product.search:
            if keywords_link:
                keywords_link = keywords_link + "-" + item
            else:
                keywords_link = item

        keywords_link = keywords_link + '/'
        self.link = self.link + keywords_link + self.price_st + product.price_st + self.price_end + product.price_end
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
