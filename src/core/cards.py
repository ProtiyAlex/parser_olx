from loguru import logger
from db.table.product_card import ProductCard as card_table
from datetime import datetime as dt
from time import sleep
from services.temlate_sms import TelegrammSms


class Cards:
    def __init__(self, db):
        self.attr = {'tag': 'div',
                     'attrs': {'data-cy': 'l-card'}}
        self.db = db

    def examination_title(self, title, search_title):
        # Преобразование всех слов в списке SEARCH к нижнему регистру
        search_lower = set(word.lower() for word in search_title)
        # Преобразование строки к нижнему регистру и разбиение на слова
        words_in_string = set(title.lower().split())
        # Проверка наличия всех слов из списка в строке
        all_words_present = all(word in words_in_string for word in search_lower)

        return all_words_present

    def parser_card(self, soup):
        try:
            card_t = card_table()
            card_t.img_link = soup.find('div', class_='css-gl6djm').find('img')['src']
            card_t.title = soup.find('h6').text
            card_t.price = soup.find('p', attrs={'data-testid': "ad-price"}).text
            card_t.location = soup.find('p', attrs={'data-testid': "location-date"}).text
            card_t.data = dt.now()
            card_t.link = soup.find('a', class_="css-rc5s2u").get('href')
            return card_t
        except Exception as e:
            logger.error(f"карточка не спарсилась {e}")
            sleep(60)

    def examination_link(self, card):
        link = self.db.get_link(card.link)
        return link
        pass

    def search_cards(self, soup, search_title):
        cards = soup.find_all(self.attr['tag'], attrs=self.attr['attrs'])

        for soup_card in cards:
            card_table = self.parser_card(soup_card)
            if not card_table:
                continue
            if self.examination_link(card_table):
                continue
            if self.examination_title(card_table.title, search_title):
                self.db.add(card_table)
                TelegrammSms(card_table)
                sleep(5)
                pass

            # pass .strftime('%Y-%m-%d %H:%M')
        pass
