# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:31:26 2020

@author: nicolás niño
"""

from selenium import webdriver
import time
import numpy as np
import pandas as pd

products = []
prices_old = []
prices_exito = []
prices_new = []
units = []
urls = []
categories = []

def get_items(containers):
    for item in containers:
        categories.append(site.split('/')[4])
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
            try:
                price_exito = item.find_element_by_xpath(".//div[@class='flex f5 fw5 pa0 flex items-center justify-start w-100 search-result-exito-vtex-components-selling-price exito-vtex-components-4-x-alliedDiscountPrice']/span").text
                prices_exito.append(price_exito)
            except:
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
            
        try:
            url = item.find_element_by_xpath(".//a").get_attribute('href')
            urls.append(url)
        except:
            urls.append(np.nan)

op = webdriver.ChromeOptions()
op.add_argument('headless')
browser = webdriver.Chrome(executable_path=r'C:\Users\nicol\Downloads\chromedriver.exe',
                           options=op)

sites = ['https://www.exito.com/tecnologia/drones',
         'https://www.exito.com/tecnologia/televisores',
         'https://www.exito.com/tecnologia/celulares',
         'https://www.exito.com/tecnologia/computadores-y-accesorios',
         'https://www.exito.com/tecnologia/audio-y-video',
         'https://www.exito.com/tecnologia/consolas-y-videojuegos',
         'https://www.exito.com/tecnologia/audio-y-video/camaras',
         'https://www.exito.com/electrodomesticos/grandes-electrodomesticos',
         'https://www.exito.com/electrodomesticos/pequenos-electrodomesticos',
         'https://www.exito.com/hogar/muebles',
         'https://www.exito.com/hogar/ropa-hogar',
         'https://www.exito.com/hogar/decoracion',
         'https://www.exito.com/hogar/mesa',
         'https://www.exito.com/hogar/cocina',
         'https://www.exito.com/moda-y-accesorios/moda-mujer',
         'https://www.exito.com/moda-y-accesorios/moda-hombre',
         'https://www.exito.com/moda-y-accesorios/moda-nina',
         'https://www.exito.com/moda-y-accesorios/moda-nino',
         'https://www.exito.com/moda-y-accesorios/perfumeria-y-accesorios',
         'https://www.exito.com/moda-y-accesorios/marroquineria',
         'https://www.exito.com/salud-y-belleza/cosmeticos-y-maquillaje',
         'https://www.exito.com/salud-y-belleza/higiene-intima',
         'https://www.exito.com/salud-y-belleza/cuidado-oral',
         'https://www.exito.com/salud-y-belleza/cuidado-capilar',
         'https://www.exito.com/salud-y-belleza/cuidado-corporal',
         'https://www.exito.com/salud-y-belleza/tratamientos',
         'https://www.exito.com/salud-y-belleza/cuidado-corporal/proteccion-solar',
         'https://www.exito.com/salud-y-belleza/drogueria',
         'https://www.exito.com/suministros-medicos',
         'https://www.exito.com/bebes',
         'https://www.exito.com/jugueteria',
         'https://www.exito.com/salud-y-belleza/panales-y-panitos',
         'https://www.exito.com/marcas-destacadas-bebes',
         'https://www.exito.com/bicicletas',
         'https://www.exito.com/deportes/acondicionamiento-fisico',
         'https://www.exito.com/deportes/camping',
         'https://www.exito.com/deportes/otros-deportes',
         'https://www.exito.com/libros-y-papeleria',
         'https://www.exito.com/ferreteria/herramientas']

for site in sites:
    
    print(site)
    
    finished=False
    n=1
    
    while finished==False: 
        try:
            site_ = site + '?page=%s' %n
            browser.get(site_)
            time.sleep(20)
            
            if browser.find_elements_by_xpath("//article[@class='vtex-product-summary-2-x-element pointer pt3 pb4 flex flex-column h-100']") == []:
                finished = True
            
            containers = browser.find_elements_by_xpath("//section[@class='vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc']")
            get_items(containers)
    
            print('Number of sites visted: %s' %n)
            n+=1
            
        except Exception as e: 
            print(e)
            print(site)

dict_ = {'product': products, 
         'price_old':prices_old, 
         'price_exito':prices_exito, 
         'price_others':prices_new, 
         'unit':units,
         'url': urls,
         'category': categories}

data_exito = pd.DataFrame(dict_)
data_exito.to_csv(r'C:\Users\nicol\Documents\0. Data\exito_total.csv')

#8142 Resultados