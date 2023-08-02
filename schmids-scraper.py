# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import itertools
import datetime

# %%
categories = {"burger": "https://harrytogo.at/schmids/burger/",
              "pastrami": "https://harrytogo.at/schmids/pastrami/",
              "bowls": "https://harrytogo.at/schmids/bowls/",
              "mains": "https://harrytogo.at/schmids/mains/",
              "curry": "https://harrytogo.at/schmids/curry/",
              "soups": "https://harrytogo.at/schmids/soups/",
              "salads": "https://harrytogo.at/schmids/salads/",
              "sweets": "https://harrytogo.at/schmids/sweets/",
              "saucen": "https://harrytogo.at/schmids/saucen/",
              "extras": "https://harrytogo.at/schmids/sides-extras/"}

burgerTable = "wcpt_deb1c3d304b017cd_1"
saucenTable = "wcpt_ec34bdda8dbd0dc6_2"

bowlTable = "wcpt_c43b4539626b570a_1"
bowlExtrasTable = "wcpt_992595051c8ebcbd_2"

mainsTable = "wcpt_5c869169cc89e466_1"

saladsTable = "wcpt_8bd6ca349eb67f88_1"
sideSaladsTable = "wcpt_6b36ae00291fd6c6_2"

pastramiTable = "wcpt_134b85755e04546d_1"

extrasTable = "wcpt_fcb6c842385d3a7c_1"

starterTable = "wcpt_a2b4c45fe5ce824f_1"
soupTable = "wcpt_35d24b17acf8ac67_2"

curryTable = "wcpt_0a342958cda7fee6_1"

sweetsTable = "wcpt_0ee473449c071b91_1"

saucenPageTable = "wcpt_ec34bdda8dbd0dc6_1"

preisMenü = float(8.9)
preisMenüMitSuppe = float(10.8)

hauptspeisenManual = list()
hauptspeisenManual.append(["Menü 1 (mit Suppe)", "", preisMenüMitSuppe])
hauptspeisenManual.append(["Menü 2 (mit Suppe)", "", preisMenüMitSuppe])
hauptspeisenManual.append(["Menü 3 (mit Suppe)", "", preisMenüMitSuppe])
hauptspeisenManual.append(["Menü 1 (ohne Suppe)", "", preisMenü])
hauptspeisenManual.append(["Menü 2 (ohne Suppe)", "", preisMenü])
hauptspeisenManual.append(["Menü 3 (ohne Suppe)", "", preisMenü])
hauptspeisenManual.append(["Miss you Menü", "", preisMenü])

extrasManual = list()
extrasManual.append(["Barbie Que Soß", "A, F, M", float(1.8)])
extrasManual.append(["Red Bull", "", float(3.36)])


# %%
def getNameDescPrice(webElement):
    name = webElement.find_element(
        By.CSS_SELECTOR, ".col-name").get_attribute("innerText")
    desc = webElement.find_element(
        By.CSS_SELECTOR, ".col-short-description").get_attribute("innerText").replace("\n", "")
    price = webElement.find_element(
        By.CSS_SELECTOR, ".col-price bdi").get_attribute("innerText").replace("€", "").strip()

    return [name, desc, float(price.replace(",", "."))]


def getDataFromTable(driver, tableid):
    wait = WebDriverWait(driver, 15)
    tbody = wait.until(ec.visibility_of_element_located(
        (By.CSS_SELECTOR, f"#{tableid} tbody")))
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    data = list()
    for row in rows:
        data.append(getNameDescPrice(row))

    return data;


def writeToFile(data, filename):
    text = ""
    for i in data:
       a = i[0]
       b = i[1].replace("\n", "")
       c = str(i[2]).replace(".", ",")
       text += f"{a};{b};{c}" + "\n"

    file = open(filename, "w",encoding="utf-8")
    file.write(text)

def getHauptspeisenFileName():
    return f"Hauptspeisen_{datetime.datetime.today().strftime('%Y-%m-%d')}.txt"

def getExtrasFileName():
    return f"Extras_{datetime.datetime.today().strftime('%Y-%m-%d')}.txt"

# %%
def getAllData(driver):
    driver.get(categories["burger"])
    burger = getDataFromTable(driver, burgerTable)
    saucen = getDataFromTable(driver, saucenTable)

    driver.get(categories["bowls"])
    bowls = getDataFromTable(driver, bowlTable)
    bowlExtras = getDataFromTable(driver, bowlExtrasTable)

    driver.get(categories["mains"])
    mains = getDataFromTable(driver, mainsTable)

    driver.get(categories["salads"])
    salads = getDataFromTable(driver, saladsTable)
    saladSides = getDataFromTable(driver, sideSaladsTable)

    driver.get(categories["pastrami"])
    pastrami = getDataFromTable(driver, pastramiTable)

    driver.get(categories["soups"])
    starters = getDataFromTable(driver, starterTable)
    soups = getDataFromTable(driver, soupTable)

    driver.get(categories["curry"])
    curry = getDataFromTable(driver, curryTable)

    driver.get(categories["sweets"])
    sweets = getDataFromTable(driver, sweetsTable)

    driver.get(categories["extras"])
    extrasPage = getDataFromTable(driver, extrasTable)

    driver.get(categories["saucen"])
    saucenPage = getDataFromTable(driver, saucenPageTable)

    hauptspeisen = list(
        itertools.chain(burger, mains, bowls, salads, pastrami, starters,
                        soups, curry, hauptspeisenManual))
    extras = list(
        itertools.chain(saucenPage, saucen, extrasPage, bowlExtras, saladSides,
                        sweets, extrasManual))

    hauptspeisenNamen = dict.fromkeys([i[0] for i in hauptspeisen], 0)
    extrasNamen = dict.fromkeys([i[0] for i in extras], 0)

    hauptspeisen_filtered = list()
    extras_filtered = list()

    for i in hauptspeisen:
        if hauptspeisenNamen[i[0]] > 0:
            continue
        hauptspeisenNamen[i[0]] += 1
        hauptspeisen_filtered.append(i)

    for i in extras:
        if extrasNamen[i[0]] > 0:
            continue
        extrasNamen[i[0]] += 1
        extras_filtered.append(i)

    writeToFile(hauptspeisen_filtered, getHauptspeisenFileName())
    writeToFile(extras_filtered, getExtrasFileName())
    

# %%
    
driver = webdriver.Edge()

getAllData(driver)

driver.close()