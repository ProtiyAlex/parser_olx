from utilities.web_draver import WebDriverClient, WebDriverClientWindow
from utilities.soup_bs import Soup
from bs4 import BeautifulSoup
from loguru import logger

from db.dbmanager import DBManager
from db.table.product_card import ProductCard
from db.table.link import Link
from setings.config import GLOBAL_LINK

from time import sleep
from datetime import datetime as dt, timedelta as td
import re


class ProductData:
    def __init__(self, type_1, type_2):
        self.type_1 = type_1
        self.type_2 = type_2
        self.title = None
        self.sku = None
        self.price = None
        self.img_link = None
        self.description = None


class ParsePage:
    def __init__(self, type_section, card, soup_fn, mian_category):
        self.mian_category = mian_category
        self.p_d = ProductData(type_section[1], type_section[2])
        self.global_link = GLOBAL_LINK
        self.soup_card = card
        self.soup = soup_fn
        self.link_page = None
        self.parse()
        pass

    def search_link_page(self):
        a = self.soup_card.find_all('a', {
            'class': 'vtmn-block vtmn-w-full vtmn-no-underline gt-small-desktop:vtmn-leading-normal vtmn-uppercase product-title'})
        self.link_page = self.global_link + a[0].get('href')
        # self.link_page = 'https://www.decathlon.co.uk/p/women-s-fitness-cardio-short-sleeved-cropped-t-shirt/_/R-p-339231?mc=8757084'
        pass

    def search_description(self, soup):

        description = ""
        try:
            description_p = soup.find_all('p', {
                'class': 'product-description'})

            for item in description_p:

                if description == "":
                    description = item.get_text()
                else:
                    description = description + " " + item.get_text()
                pass
        except Exception as e:
            logger.error(f"не спарсился description {e}")
        return description

    def sku(self, soup):
        try:
            sku = soup.find_all('span', {
                'class': 'current-selected-model'})
            if sku:
                sku = sku[0].get_text().replace('Ref. : ', '').strip()
                return sku
        except Exception as e:
            logger.error(f"не спарсился sku {e}")

    def title(self, soup):
        return soup.h1.get_text()

    def price(self, soup):
        try:
            price = soup.find_all('span', {
                'aria-label': 'price'})  # {'class': 'vtmn-price vtmn-price_size--medium vtmn-price_variant--accent'}
            price = price[0].get_text().strip()
            price = ''.join(re.findall(r'[\d.,]+', price))
            return price
        except Exception as e:
            logger.error(f"не спарсился price {e}")

    def img(self, soup,link):
        try:
            img_link = ""

            search_options = [
                {'tag': 'div', 'class': 'slides svelte-17gwspz'},
                {'tag': 'ul', 'class': 'swiper-wrapper'},

            ]

            img = None

            for search_option in search_options:
                try:
                    img = soup.find(search_option['tag'], {'class': search_option['class']}).find_all('img')
                    if img:
                        break
                except AttributeError:
                    continue



            for item in img:
                if img_link == "":
                    img_link = item['src']
                else:
                    img_link = img_link + ", " + item['src']
            return img_link

        except Exception as e:
            logger.error(f"не спарсился img_link {e}: {link}")

    def check_link_db(self):
        link_record = DBManager().get_link(self.link_page)

        if link_record:
            # Если запись с нужным линком найдена
            current_date = dt.now().date()  # Получаем текущую дату без времени
            end = link_record.data_end.date()  # Получаем дату из записи без времени
            start = link_record.data_start.date()

            if start <= current_date <= end:

                # Если дата в записи совпадает с текущей датой
                return True
            else:
                DBManager().del_row_(link_record)
                # Если дата в записи не совпадает с текущей датой
                return False
        else:
            # Если запись с нужным линком не найдена
            return False

    def parse(self):
        self.search_link_page()
        if self.check_link_db():
            logger.debug(f"Ссылка в базе {self.link_page}")
            return
        soup = self.soup.get_soup(self.link_page)

        self.p_d.description = self.search_description(soup)
        self.p_d.sku = self.sku(soup)
        self.p_d.title = self.title(soup)
        self.p_d.price = self.price(soup)
        self.p_d.img_link = self.img(soup,self.link_page)

        self.write_madel_db(self.p_d)
        pass

    def write_madel_db(self, pd):
        pd_model = ProductCard()
        pd_model.type_1 = pd.type_1
        pd_model.type_2 = pd.type_2
        pd_model.sku = pd.sku
        pd_model.title = pd.title
        pd_model.price = pd.price
        pd_model.img_link = pd.img_link
        pd_model.description = pd.description
        pd_model.main_category = self.mian_category

        pd_model.link = self.link_page
        pd_model.data_start = dt.now().date()
        pd_model.data_end = dt.now().date() + td(days=7)

        DBManager().add(pd_model)
        pass


class Section:
    def __init__(self, mian_category):
        self.mian_category = mian_category
        self.count_page = None
        self.soup = Soup()
        # self.wbw = WebDriverClientWindow()
        pass

    def fn_long_section(self, url):

        soup = self.soup.get_soup(url)
        try:
            a = soup.find_all('a', class_='svelte-172u1kv')
            self.count_page = int(a[-1].text.strip())
            logger.info(f"{url} кол-во страниц {self.count_page}")
            return soup
            pass
        except Exception as e:

            logger.info(f"{e} на ссылке {url} не найдено кол-во страниц или она одна")
            return soup

    def parse_card(self, soup, type_section):
        # page_card = soup.find('section',{'class':'listing-section'}).find_all('div', {
        #     'class': 'vtmn-flex vtmn-flex-col vtmn-items-center vtmn-relative vtmn-overflow-hidden vtmn-text-center vtmn-z-0 dpb-holder svelte-id5od5'})

        page_card = soup.find_all('div', {
            'class': 'vtmn-flex vtmn-flex-col vtmn-items-center vtmn-relative vtmn-overflow-hidden vtmn-text-center vtmn-z-0 dpb-holder svelte-id5od5'})

        for card in page_card:
            try:
                parse_page = ParsePage(type_section, card, self.soup,self.mian_category)
                logger.debug(f"спарсилась очередная карточка из {type_section[1]}, {type_section[2]}")

            except Exception as e:
                logger.error(f"Ошибка парсинга страницы: {e}: {parse_page.link_page}")
                sleep(10)

    def parse_page(self, url, type_section):
        soup = self.soup.get_soup(url)

        return self.parse_card(soup, type_section)
