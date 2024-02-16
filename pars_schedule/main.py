import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)
base_url = 'https://mtuci.ru/time-table/'
driver.get(base_url)

#l = driver.find_element(By.XPATH,"//div[contains(text(),'Очная')]")
#driver.execute_script("arguments[0].click();", l);

WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(),'Очная')]"))).click()

WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(),'Информационные технологии')]"))).click()

WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "(//div[contains(text(),'Второй')])[3]"))).click()

WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "(//div[contains(text(),'Занятия')])[8]"))).click()

WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(),'БФИ2201')]"))).click()
