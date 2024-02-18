import time

import pypdf as pyPdf
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import io
import PyPDF2

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)
base_url = 'https://mtuci.ru/time-table/'
driver.get(base_url)

#l = driver.find_element(By.XPATH,"//div[contains(text(),'Очная')]")
#driver.execute_script("arguments[0].click();", l);
time.sleep(1)

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


'''
response = requests.get(str(l))
pdf_io_bytes = io.BytesIO(response.content)
text_list = []
pdf = PyPDF2.PdfReader(pdf_io_bytes)

num_pages = len(pdf.pages)

for page in range(num_pages):
    page_text = pdf.pages[page].extract_text()
    text_list.append(page_text)
text = "\n".join(text_list)
print(text)
'''


import urllib3
urllib3.disable_warnings()

with urllib3.PoolManager() as http:
    r = http.request('GET', l)
    with io.BytesIO(r.data) as f:
        reader = PyPDF2.PdfReader(f)
        contents = reader.pages[0].extract_text().split('\n')


print('\n'.join(contents))