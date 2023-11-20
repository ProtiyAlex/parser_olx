import os

BASE_DIR = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
DATABASE = os.path.join('sqlite:///' + BASE_DIR, "data.db")
FILENAME_LOG = os.path.join(BASE_DIR, "log.txt")

# _________________________________________________

# _________________________________________________
GLOBAL_LINK = 'https://www.olx.ua'
ITER_LINK = ['/list/q-',
             '?search%5Bfilter_float_price:from%5D=',
             '&search%5Bfilter_float_price:to%5D=',
             "?page=",
             '&search%5Bfilter_float_price%3Afrom%5D=',
             '&search%5Bfilter_float_price%3Ato%5D='
             ]


# 10000&search%5Bfilter_float_price:to%5D=100000
# _________________________________________________
SEARCH = ['garmin', 'epix']
PRICE = [10000, 26000]  # in UAN



