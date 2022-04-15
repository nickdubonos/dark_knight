import re
import sqlite3
from classifer import vectorization
from classifer import mnb
from aiogram.dispatcher.filters.state import  StatesGroup,State


class Dialog(StatesGroup):
    S1=State()
    S2=State()

class BotDB:

    def __init__(self, db_fale):
        self.conn = sqlite3.connect(db_fale)
        self.cursor = self.conn.cursor()


    def url(self, url):
        """Проверяем, есть ли url в базе"""
        result = self.cursor.execute("SELECT `url` FROM `URL` WHERE `url` = ?", (url,))
        return bool(len(result.fetchall()))

    def label(self, fas):
        """Проверяем label в базе"""
        result=self.cursor.execute("SELECT `label` FROM `URL` WHERE `url` = ?", (fas,))
        if result.fetchone()[0]==1:
            return True
        else:
            return False

    def f(self,url):
        result = self.cursor.execute("SELECT `label` FROM `URL` WHERE `url` = ?", (url,))
        return result.fetchone()



    def add_url(self, text,label):
        """Добавляем url в базу"""
        self.cursor.execute("INSERT INTO URL (url,label) VALUES (?,?)", (text,label))
        return self.conn.commit()

    def classification(self,olol):
        """Используем классификатор"""
        testing_pr=[str(olol)]
        pred = mnb.predict(vectorization.transform(testing_pr))
        if int(pred[0])==1:
            return True
        else:
            return False

    def is_url(self,url):
        """Проверяем является ли сообщение url"""
        url=re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',url)
        if url is not None:
            return True
        else:
            return False


    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
        return self.conn.commit()

