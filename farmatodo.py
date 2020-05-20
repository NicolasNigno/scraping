# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:55:37 2020

@author: nicol

Farmatodo scraper
"""

from selenium import webdriver
import time
import pandas as pd
import numpy as np
from price_parser import Price
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://www.farmatodo.com.co/categorias/cuidado-personal/higiene-personal/proteccion-femenina'
browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe')
browser.get(url)

time.sleep(30)
timeout=60

n=0
more = True
while more:
    elem = WebDriverWait(browser, timeout).until(lambda x: x.find_elements_by_xpath("//button[@class='cont-button-more my-5']"))
    elem[0].click()
    n+=1
    print('He dado %s clicks' %n)

    if browser.find_elements_by_xpath("//button[@class='cont-button-more my-5']")==[]: 
        more = False

    time.sleep(5)

time.sleep(30)

containers = browser.find_elements_by_xpath("//div[@class='card-ftd mb-3']")

products = []
descriptions = []
prices = []
units = []

for items in containers:
    try:
        product = items.find_element_by_xpath('.//p[@class="text-title"]').text
        products.append(product)
    except:
        products.append(np.nan)

    try:
        description = items.find_element_by_xpath('.//p[@class="text-description"]').text
        descriptions.append(description)
    except:
        descriptions.append(np.nan)

    try:
        price = items.find_element_by_xpath('.//span[@class="text-price"]').text
        prices.append(price)
    except:
        prices.append(np.nan)

    try:
        unit = items.find_element_by_xpath('.//p[@class="text-price-unit"]').text
        units.append(unit)
    except:
        units.append(np.nan)

dict_ = {'products': products, 'descriptions':descriptions, 'prices':prices, 'units':units}
data_farmatodo = pd.DataFrame(dict_)

def getvalue(x):
    try:   
        return Price.fromstring(x).amount_float
    except: 
        return None

data_farmatodo['price_new'] = data_farmatodo['prices'].apply(lambda x: getvalue(x))