# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:55:37 2020

@author: nicol

Farmatodo scraper
"""

from selenium import webdriver
import time
import pandas as pd
from price_parser import Price
from bs4 import BeautifulSoup
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

productos = browser.find_elements_by_xpath("//div[@class='card-ftd mb-3']")
productos = [x.text for x in productos]