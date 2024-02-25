from datetime import timedelta
import re
import datetime
from math import ceil

import pdfplumber
import pyjokes
import requests
import translator as translator
from bs4 import BeautifulSoup
from googletrans import Translator


def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

def table_converter(table):
    table_string = [[],[],[],[],[],[]]
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string[row_num // 5].append(cleaned_row)

    return table_string


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


from fake_useragent import UserAgent


url = 'https://mtuci.ru/time-table/' # url для второй страницы
r = requests.get(url, headers={'User-Agent': UserAgent().edge})
html = r.content

soup = BeautifulSoup(html,'html.parser')
obj = soup.find(href=re.compile(("BFI2201.pdf")))

s = obj.get('href')
result = 'https://mtuci.ru/' + s


def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    year, month, day = date.split('-')
    day = day.split(' ')[0]
    return f'{day} {months[int(month) - 1]} {year} года'


d1 = datetime.datetime(2024, 1, 28)
d2 = datetime.datetime.now()

even = 'нечётная'
parity = ceil((d2 - d1).days / 7)
if not (parity) % 2:
   even = 'чётная'

days = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']






