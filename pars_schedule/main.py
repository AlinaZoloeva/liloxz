import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTRect
import pdfplumber
import os
from tmp import extract_table, table_converter



options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)
base_url = 'https://mtuci.ru/time-table/'
driver.get(base_url)

time.sleep(1) # страница не всегда успевает подгружаться, поэтому небольшая пауза
WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'Очная')]"))).click()
time.sleep(1)
WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(),'Информационные технологии')]"))).click()
time.sleep(1)
WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "(//div[contains(text(),'Второй')])[3]"))).click()
time.sleep(1)
WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "(//div[contains(text(),'Занятия')])[8]"))).click()
time.sleep(1)
l = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.LINK_TEXT, 'БФИ2201'))).get_attribute('href')



################ ИЗВЛЕЧЕНИЕ ДАННЫХ ИЗ PDF ######################
dirname = str(os.getcwd())
print(os.getcwd())
filename = dirname +  '\\tmp\\bfi2201.pdf'
print(filename)
url = str(l)

response = requests.get(url)

with open(filename, 'wb') as f:
    f.write(response.content)


pdf_path = filename

pdfFileObj = open(pdf_path, 'rb')
pdfReaded = PyPDF2.PdfReader(pdfFileObj)

for pagenum, page in enumerate(extract_pages(pdf_path)):
    pageObj = pdfReaded.pages[pagenum]
    # Инициализируем количество исследованных таблиц
    table_num = 0
    first_element = True
    table_extraction_flag = False

    pdf = pdfplumber.open(pdf_path)

    page_tables = pdf.pages[pagenum] # Находим исследуемую страницу
    tables = page_tables.find_tables() # Количество страниц

    page_elements = [(element.y1, element) for element in page._objs]

    page_elements.sort(key=lambda a: a[0], reverse=True)

    for i, component in enumerate(page_elements):
        pos = component[0]
        element = component[1]

        if isinstance(element, LTRect):
            if first_element == True and (table_num + 1) <= len(tables):
                # Находим ограничивающий прямоугольник таблицы
                lower_side = page.bbox[3] - tables[table_num].bbox[3]
                upper_side = element.y1
                # Извлекаем информацию из таблицы
                table = extract_table(pdf_path, pagenum, table_num)
                # удалем первые две записи, так как они не представляют ценности
                table.pop(0)
                table.pop(0)
                table_text = table_converter(table)

                table_extraction_flag = True
                first_element = False

            # Проверка извлечения таблиц из страницы
            if element.y0 >= lower_side and element.y1 <= upper_side:
                pass
            elif not isinstance(page_elements[i + 1][1], LTRect):
                table_extraction_flag = False
                first_element = True
                table_num += 1

pdfFileObj.close()


############ Упорядочивание данных ####################
for i in range(6):
    for j in range(5):
        table_text[i][j].pop(0)

table_res = [[], [], [], [], [], []]
for i in range(6):
    for j in range(5):
        table_res[i].append(table_text[i][j][:6])
        table_res[i].append(table_text[i][j][6:])

for i in range(6):
    for j in range(1, 11, 2):
        table_res[i][j].insert(0, table_res[i][j - 1][1])
        table_res[i][j].insert(0, table_res[i][j - 1][0])
print(table_res)

