

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


from selenium import webdriver
from selenium.webdriver.chrome.service import Service


import requests
from time import sleep


class WebDriverClientWindow:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self._driver = webdriver.Chrome(service=Service(), options=options)

    def dispose(self):
        self._driver.close()
        self._driver.quit()

    def get_response(self, url):
        try:
            self._driver.get(url)
            sleep(2)
            # Получите HTML-код страницы
            html = self._driver.page_source

            # Создайте объект BeautifulSoup для парсинга

            return html


        except Exception as ex:
            return False
        # finally:
        #     sleep(2)
        #     self._driver.close()
        #     self._driver.quit()


class WebDriverClient:
    def __init__(self):
        self._timeout = 20

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.set_capability('acceptInsecureCerts', True)
        # dr = ChromeDriverManager().install()
        # service = Service()
        # options = webdriver.ChromeOptions()
        self._driver = webdriver.Chrome(service=Service(), options=options)

        # options = Options()
        # options.add_argument("start-maximized")
        # self._driver = webdriver.Chrome(options=options)
        # driver.get("https://www.google.com/")



        # self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self._driver.set_page_load_timeout(self._timeout)

    def dispose(self):
        self._driver.close()
        self._driver.quit()

    def get_response(self, url):


        try:
            driver = self._driver
            driver.get(url)

            # Прокрутка страницы вниз, чтобы загрузить все элементы
            # Вы можете изменить количество прокруток, если требуется
            for _ in range(11):  # Пример: 5 прокруток
                driver.execute_script("window.scrollBy(0, 900);")
                # driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                sleep(4)  # Подождать, чтобы страница загрузилась после каждой прокрутки

            # Получение HTML-кода страницы после прокрутки
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            return html, soup

        except Exception as ex:
            return '', ''
        # try:
        #     driver = self._driver
        #
        #     driver.get(url)
        #
        #
        #     try:
        #         driver.execute_script("window.__cfRLUnblockHandlers = true;")
        #
        #
        #         html_doc = BeautifulSoup(driver.page_source, 'html.parser')
        #         text = html_doc.get_text()
        #
        #         if len(text) < 200:
        #             sleep(2)
        #     except:
        #         pass
        #
        #
        #
        #     text_content = ''
        #
        #     try:
        #         text_content = driver.find_element(By.TAG_NAME, "body").text
        #     except:
        #         pass
        #
        #     return driver.page_source, text_content
        # except:
        #     return '', ''