# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:15:29 2020

@author: nicolás niño
"""

from selenium import webdriver
import time
import pandas as pd
from price_parser import Price
import numpy as np

products = []
prices_old = []
prices_exito = []
prices_new = []
units = []

## Página 1 ##

def get_items(containers):
    for item in containers:
        try:
            product = item.find_element_by_xpath(".//span[@class='vtex-store-components-3-x-productBrand f6 fw5 shelfProductName search-result-exito-product-summary-name-product']").text
            products.append(product)
        except:
            products.append(np.nan)

        try:
            price_new = item.find_element_by_xpath(".//div[@class='flex f5 fw5 pa0 flex items-end justify-start w-100 search-result-exito-vtex-components-other-selling-price exito-vtex-components-4-x-otherSellingPrice']/span[1]").text
            prices_new.append(price_new)
        except:
            prices_new.append(np.nan)

        try:
            price_exito = item.find_element_by_xpath(".//div[@class='flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-allies-discount exito-vtex-components-4-x-alliedDiscountPrice']/span").text
            prices_exito.append(price_exito)
        except:
            prices_exito.append(np.nan)

        try:
            price_old = item.find_element_by_xpath(".//span[@class='flex w-100 c-muted-2 mb0 fw5 t-mini ttn search-result-exito-vtex-components-list-price exito-vtex-components-4-x-priceTag exito-vtex-components-4-x-priceTagDel']/del/span").text
            prices_old.append(price_old)
        except:
            prices_old.append(np.nan)

        try:
            unit = item.find_element_by_xpath(".//div[@class='exito-vtex-components-4-x-mainContainerProductPum']/div").text
            units.append(unit)
        except:
            units.append(np.nan)

url = 'https://www.exito.com/salud-y-belleza/higiene-intima'
browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe')
browser.get(url)

time.sleep(10)

containers = browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']")

get_items(containers)

browser.quit()

## Resto de páginas ##

finished = False
n=2

while finished == False:
    try:
        url = 'https://www.exito.com/salud-y-belleza/higiene-intima?page=%s' %n
        browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe')
        browser.get(url)
        
        time.sleep(20)
        if browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']") == []:
            finished = True
        
        containers = browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']")
        get_items(containers)
        
        n+=1
        
        time.sleep(2)
        
        browser.quit()
    except:
        pass

dict_ = {'products': products, 'prices_old':prices_old, 'prices_exito':prices_exito, 'prices_new':prices_new, 'units':units}
data_exito = pd.DataFrame(dict_)

def getvalue(x):
    try:   
        return Price.fromstring(x).amount_float
    except: 
        return None

data_exito['prices_old_2'] = data_exito['prices_old'].apply(lambda x: getvalue(x))
data_exito['prices_exito_2'] = data_exito['prices_exito'].apply(lambda x: getvalue(x))
data_exito['prices_new_2'] = data_exito['prices_new'].apply(lambda x: getvalue(x))

def getunidad(x):
    try:
        x = x.replace(',', '.')
        position = x.index('$')
        x = x[position+1:].strip()
        return float(x)
    except:
        return None

data_exito['units_2'] = data_exito['units'].apply(lambda x: getunidad(x))

