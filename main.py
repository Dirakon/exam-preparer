import requests
import selenium
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome(ChromeDriverManager().install())



url = 'https://rus-ege.sdamgia.ru'


driver.get(url)

webpage = driver.page_source


soup = BeautifulSoup(webpage,features="lxml")

film_list = driver.find_elements_by_class_name('Counter')
print(film_list)

driver.close()