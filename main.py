import requests
import selenium
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome(ChromeDriverManager().install())

#driver.minimize_window()
def openQuest(num):
    global url

    driver.get(url)

    time.sleep(0.1)

    webpage = driver.page_source


    questList = driver.find_elements_by_class_name('Counter')

    needed = questList[num]
    counterButtons = needed.find_elements_by_class_name('Counter-Button')
    counterButtons[1].click()

    time.sleep(0.1)

    goFutherButton = driver.find_element_by_xpath("//button[@type='submit']")

    goFutherButton.click()

    time.sleep(0.1)



    texts_mainB = driver.find_element_by_xpath("//div[@class='prob_maindiv']")
    texts = texts_mainB.find_elements_by_class_name('left_margin')[:-1]
    textsExtra = texts_mainB.find_elements_by_tag_name('i')

    superText = ""

    for i in texts:
        superText += i.get_attribute('innerHTML') + '\n'
    for i in textsExtra:
        superText +=i.get_attribute('innerHTML') + '\n'
    return superText

def inputAnswer(ans):

    inputField = driver.find_element_by_xpath("//input[@size='50']")
    inputField.send_keys(ans)
    goFutherButton = driver.find_element_by_xpath("//input[@value='Сохранить']")
    goFutherButton.click()
    possibleTexts = driver.find_elements_by_tag_name('td')
    for i in possibleTexts:
        intrestingProprerty = str(i.get_attribute('style'))
        if intrestingProprerty.startswith('text-align') and 'background' in intrestingProprerty:
            if ('255, 192, 192' in intrestingProprerty):
                #we got it wrong my guys...
                print("Неверно...")
            else:
                #correct!
                print("Верно!")
        #=='text-align:center;background:#ffc0c0'


url = 'https://rus-ege.sdamgia.ru'

print(openQuest(0))
inputAnswer(input('Ответ: '))

time.sleep(100)
driver.close()