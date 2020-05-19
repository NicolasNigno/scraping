# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:15:29 2020

@author: nicolás niño
"""

from selenium import webdriver
import time
import pandas as pd
from price_parser import Price

## Página 1 ##

url = 'https://www.exito.com/salud-y-belleza/higiene-intima'
browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe')
browser.get(url)

time.sleep(10)

exito = browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']")
productos = [x.text for x in exito]

time.sleep(2)

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
            
        exito = browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']")
        productos_ = [x.text for x in exito]
        
        productos = productos + productos_
        
        n+=1
        
        time.sleep(2)
        
        browser.quit()
    except:
        pass
      
## Arreglar datos

column_names = ['producto', 'precio 1', 'precio 2', 'unidades', 'info extra']

datos_exito = pd.DataFrame(columns = column_names)

productos_new = [x.split('\n') for x in productos]

j=0
for info in productos_new:
   for i in info:
       prices = [x for x in info if x.startswith("$")]
       
       try: datos_exito.loc[j, 'precio 1'] = prices[0]
       except: pass
       try: datos_exito.loc[j, 'precio 2'] = prices[1]
       except: pass
       
       if ('$' not in i) and ('%' not in i) and ('Unidad' not in i) and ('¡Lo quiero!' not in i):
           datos_exito.loc[j, 'producto'] = i
       elif 'Unidad' in i:
           datos_exito.loc[j, 'unidades'] = i
       elif '%' in i:
           datos_exito.loc[j, 'info extra'] = i
           
   j+=1
    

def getvalue(x):
    try:   
        return Price.fromstring(x).amount_float
    except: 
        return None

datos_exito['price 1'] = datos_exito['precio 1'].apply(lambda x: getvalue(x))
datos_exito['price 2'] = datos_exito['precio 2'].apply(lambda x: getvalue(x))

def getunidad(x):
    try:
        x = x.replace('Unidad a $ ', '')
        x = x.replace(',', '.')
        return float(x)
    except:
        return None

datos_exito['unidad'] = datos_exito['unidades'].apply(lambda x: getunidad(x))

def getdescuento(x):
    try:
        x = x.replace('%', '')
        x = float(x)
        return x/100
    except:
        return None

datos_exito['descuento'] = datos_exito['info extra'].apply(lambda x: getdescuento(x))







