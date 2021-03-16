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


file = open('settings.txt','r',encoding='utf-8')

all_settings = file.read().split('\n')

urls = {}

for setting in all_settings:
    setting = [i.strip(' ') for i in setting.split('=')]
    if 'url' in setting[0] and len(setting) > 2:
        urls[setting[1].split("'")[1]]=setting[2].split("'")[1]

print("Выберите предмет.")
ind = 1
for i in urls:
    print(ind,i)
    ind+=1

choice = 0
while choice < 1 or choice >len(urls):
    choice = int(input("Номер предмета: "))

ind = 1
for i in urls:
    if ind == choice:
        url = urls[i]
    ind += 1


def openQuest(num):
    global url

    driver.get(url)

    time.sleep(0.1)

    questList = driver.find_elements_by_class_name('Counter')

    needed = questList[num]
    counterButtons = needed.find_elements_by_class_name('Counter-Button')
    counterButtons[1].click()

    time.sleep(0.1)

    goFutherButton = driver.find_element_by_xpath("//button[@type='submit']")

    goFutherButton.click()

    time.sleep(0.1)



    texts_mainB = driver.find_element_by_xpath("//div[@class='prob_maindiv']")
    texts = texts_mainB.find_elements_by_tag_name('p')
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

    inNeedOfRightAnswer = False
    for i in possibleTexts:
        if inNeedOfRightAnswer:
            inNeedOfRightAnswer=False
            print('Правильный ответ: ',i.get_attribute('innerHTML')) # Get right answer if we failed to write it
        intrestingProprerty = str(i.get_attribute('style'))
        if intrestingProprerty.startswith('text-align') and 'background' in intrestingProprerty:
            if ('192, 255, 192)' in intrestingProprerty): # Green color
                #correct!
                print("Верно!")
            else:
                inNeedOfRightAnswer=True
                #we got it wrong my guys...
                print("Неверно...")
        #=='text-align:center;background:#ffc0c0'


print(openQuest(0))
inputAnswer(input('Ответ: '))

time.sleep(100)
driver.close()