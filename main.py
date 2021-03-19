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
import tkinter as tk


def loadSettings():
    global all_settings
    global urls
    global motivationalQuote
    file = open('settings.txt', 'r', encoding='utf-8')

    all_settings = file.read().split('\n')

    urls = {}

    for setting in all_settings:
        setting = [i.strip(' ') for i in setting.split('=')]
        if 'url' in setting[0] and len(setting) > 2:
            urls[setting[1].split("'")[1]]=setting[2].split("'")[1]
        elif 'motivational_url' in setting[0] and len(setting) > 1:
            motivationalQuote = setting[1].split("'")[1]

motivationalQuote = None
urlHasBeenChosen = False

def checkForDecision():
    global url
    global urls
    global all_settings
    global text
    global window
    global tickTime
    global urlHasBeenChosen

    choice = 0

    changedText = text.get(1.0, tk.END)

    answerPart = changedText.split('Номер предмета:')[1].split('\n')

    if len(answerPart) > 2:  # Pressed enter on the end of answerLine
        choice = int(answerPart[0].strip(' '))

    if choice < 1 or choice > len(urls):
        window.after(tickTime, checkForDecision)
        return
     #   choice = int(input("Номер предмета: "))

    ind = 1
    for i in urls:
        if ind == choice:
            url = urls[i]
        ind += 1
    urlHasBeenChosen = True

def chooseUrl():
    global url
    global urls
    global all_settings
    global window
    global text
    global tickTime
    compiled_text = "Выберите предмет.\n"
    ind = 1
    for i in urls:
        compiled_text += str(ind) + ' ' + i + '\n'
        ind += 1

    compiled_text += "Номер предмета: "

    text.insert(1.0, compiled_text)
    window.after(tickTime, checkForDecision)


def openQuest(num):
    global url

    driver.get(url)

    time.sleep(0.1)

    questList = driver.find_elements_by_class_name('Counter')
    if num != 0:
        prevNeeded = questList[num-1]
        prevCounterButtons = prevNeeded.find_elements_by_class_name('Counter-Button')
        prevCounterButtons[0].click()


    needed = questList[num]
    counterButtons = needed.find_elements_by_class_name('Counter-Button')
    counterButtons[1].click()

    time.sleep(0.1)

    goFurtherButton = driver.find_element_by_xpath("//button[@type='submit']")

    goFurtherButton.click()

    time.sleep(0.1)

    texts_mainB = driver.find_element_by_xpath("//div[@class='prob_maindiv']")
    texts = texts_mainB.find_elements_by_tag_name('p')
    textsExtra = texts_mainB.find_elements_by_tag_name('i')

    superText = ""

    for i in texts:
        superText += i.get_attribute('innerHTML') + '\n'
    for i in textsExtra:
        superText += i.get_attribute('innerHTML') + '\n'

    replaceDic = {'&lt;': '<', '&gt;': '>', '&nbsp;': ' ', '<b>': '', '<i>': '', '</i>': '', '</b>': ''}
    for i in replaceDic:
        superText = superText.replace(i, replaceDic[i])
    return superText


def inputAnswer(ans):

    inputField = driver.find_element_by_xpath("//input[@size='50']")
    inputField.send_keys(ans)
    goFurtherButton = driver.find_element_by_xpath("//input[@value='Сохранить']")
    goFurtherButton.click()
    possibleTexts = driver.find_elements_by_tag_name('td')

    inNeedOfRightAnswer = False
    for i in possibleTexts:
        if inNeedOfRightAnswer:
            return 'Неверно...\n Правильный ответ: ' + i.get_attribute('innerHTML') + '\n----------\n\n' # Get right answer if we failed to write it
        interestingProperty = str(i.get_attribute('style'))
        if interestingProperty.startswith('text-align') and 'background' in interestingProperty:
            if '192, 255, 192' in interestingProperty:  # Green color
                # correct!
                return "Верно!\n----------\n\n"
            else:
                inNeedOfRightAnswer=True
                # we got it wrong my guys...
        # =='text-align:center;background:#ffc0c0'


driver = webdriver.Chrome(ChromeDriverManager().install())

tickTime = 100

currentlyHasTask = False

firstSetupDone = False


def loadQuote():
    global motivationalQuote
    if motivationalQuote is None:
        return "Не удалось загрузить цитату..."

    return 'TO-DO: implement quote logic'


def firstLoad():
    global window
    global tickTime
    global driver
    global text
    global firstSetupDone
    global urlHasBeenChosen

    if not firstSetupDone:

        greeting = tk.Label(text=loadQuote())
        greeting.pack()

        text = tk.Text()
        text.pack()

        loadSettings()

        chooseUrl()
        firstSetupDone = True

    if not urlHasBeenChosen:
        window.after(tickTime, firstLoad)
        return

    text.delete(1.0, tk.END)
    window.after(tickTime, programTick)


numberOfTask = 0

textAppendix = ""


def programTick():
    global window
    global tickTime
    global driver
    global amountOfRows
    global text
    global currentlyHasTask
    global numberOfTask
    global textAppendix

    if not currentlyHasTask:

        print(numberOfTask)

        questText = textAppendix+openQuest(numberOfTask)
        numberOfTask += 1
        text.insert(1.0, questText)

        amountOfRows = questText.count('\n') + 1

        text.insert(float(amountOfRows), "//Ваш ответ: ")
        currentlyHasTask = True
    else:

        changedText = text.get(1.0,tk.END)

        answerPart = changedText.split('//Ваш ответ:')[1].split('\n')

        # print(len(answerPart))

        if len(answerPart) > 2:  # Pressed enter on the end of answerLine
            answerPart = answerPart[0].strip(' ')
            textAppendix = inputAnswer(answerPart)
            currentlyHasTask=False
            text.delete(1.0, tk.END)

    window.after(tickTime, programTick)


window = tk.Tk()


window.after(tickTime, firstLoad)

window.mainloop()

inputAnswer(input('Ответ: '))

time.sleep(100)
driver.close()
