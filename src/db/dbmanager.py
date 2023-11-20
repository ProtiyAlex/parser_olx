from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from os import path
from loguru import logger

from db.dbcore import Base
from setings.config import DATABASE, BASE_DIR
from utilities.singleton import Singleton
from db.table.product_card import ProductCard
import pandas as pd

from tabulate import tabulate

from datetime import datetime as dt


class DBManager(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(DATABASE)
        _Session = sessionmaker(bind=self.engine)
        self.session = _Session()
        if not path.isfile(DATABASE):
            Base.metadata.create_all(self.engine)
        logger.info("С базой данных соединились.")

    def add(self, model):
        self.session.add(model)
        self.session.commit()

    # def add_balans(self, usdt,bnb):
    #     new_row = Balans(date=dt.now().date(),
    #                      balans_usdt=usdt,
    #                      balans_bnb=bnb)
    #     self.session.add(new_row)
    #     self.session.commit()

    def del_row_(self, row):
        self.session.delete(row)
        self.session.commit()

    def del_row(self, model):
        self.session.query(model).delete()
        self.session.commit()

    def get_link(self, target_link):
        return self.session.query(ProductCard).filter_by(link=target_link).first()

    # def get_online_status(self, status):
    #     return self.session.query(OnlineTrade).filter_by(status=status).all()
    #
    #
    # def add_online(self, data):
    #     self.session.add(OnlineTrade(*data))
    #     self.session.commit()
    #     # self.close()

    def clean_old_value(self):
        selected_values = self.session.query(ProductCard).filter(ProductCard.data_end < dt.now()).all()
        for value in selected_values:
            self.session.delete(value)

        # Подтверждаем изменения
        self.session.commit()
        logger.info(f"С базы данных удалили старые записи в кол-ве {len(selected_values)}шт")

    def save_to_csv(self):
        self.clean_old_value()

        all_records = self.session.query(ProductCard).all()
        df = pd.DataFrame([record.__dict__ for record in all_records])

        # Удалите лишний столбец '_sa_instance_state'
        df = df.drop(['_sa_instance_state', 'id', 'data_start', 'data_end', 'type_1', 'type_2', 'link'], axis=1)

        csv_file_path = path.join(BASE_DIR, 'data.csv')

        # df['price'] = df['price'].str.replace('£', '')
        # print(tabulate(df.head(10), headers='keys', tablefmt='psql'))
        # Сохраните данные в CSV
        df.to_csv(csv_file_path, index=False)
        logger.info(f"Файл парсинга data.csv сформирован кол-во товаров {df.shape[0]}шт")
        return df

    def close(self):
        self.session.close()

# a = DBManager()
# b=a.get_balans()
# pass
# s = a.get_stat_pair("XRPqUSDT")
# a.add_stat_pair("XRPUSDT",1)
# pass
