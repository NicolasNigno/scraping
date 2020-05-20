# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:55:37 2020

@author: nicol
"""

from selenium import webdriver
import time
import pandas as pd
from price_parser import Price
from bs4 import BeautifulSoup

url = 'https://www.farmatodo.com.co/categorias/cuidado-personal/higiene-personal/proteccion-femenina'