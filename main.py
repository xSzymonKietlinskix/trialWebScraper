import re
import requests
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
import csv
def save_to_csv(fileName, list):
    header = ['brand']
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for l in list:
            writer.writerow([l])

def save_models_to_csv(fileName, list, marka):
    with open(fileName, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for l in list:
            if l == "Wszytskie modele" :
                continue
            row = marka + ';' + l
            writer.writerow([row])

def read_from_csv(fileName):
    list = []
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            list.append(row)
    return list
def read_marki(min_amount):
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Otwarcie strony internetowej
    driver.get('https://www.otomoto.pl/osobowe?search%5Badvanced_search_expanded%5D=true')
    # Kliknięcie ciasteczek
    cookies = driver.find_element(By.XPATH,
                                 '//*[@id="onetrust-accept-btn-handler"]')

    cookies.click()

   # time.sleep(2)
    # kliknij marki (strzałkę)
    brands_open = driver.find_element(By.XPATH,
                                 '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]')

    brands_open.click()
    #pobiera listę marek
    list_marki = driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/ul')
    marki = list_marki.find_elements(By.TAG_NAME, 'li')
    istotne_marki = []

    for marka in marki:
        l_egz = r'\((.*?)\)'
        if not marka.text == "Wszystkie marki":
            dopasowanie = re.search(l_egz, marka.text)
            if int(dopasowanie.group(1)) > min_amount:
                istotne_marki.append(marka.text)

    print(istotne_marki)
    return istotne_marki



    driver.quit()

def read_models(marki, min_amount):
    istotne_modele = []
    for marka_ in marki:
        if marka_[0] == "brand" or marka_[0] == "Alfa Romeo (1456)":
            continue
        driver = webdriver.Chrome()
        driver.maximize_window()
        # Otwarcie strony internetowej
        link = 'https://www.otomoto.pl/osobowe/'
        marka = marka_[0]
        marka = marka.lower()

        marka = re.sub(r'\([^)]*\)', '', marka)
        marka = marka.rstrip()
        marka = marka.replace(" ", "_")
        link += marka
        link += '?search%5Badvanced_search_expanded%5D=true'
        driver.get(link)
        # Kliknięcie ciasteczek
        cookies = driver.find_element(By.XPATH,
                                      '//*[@id="onetrust-accept-btn-handler"]')

        cookies.click()
        models_open = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]')
        models_open.click()
        lista_modeli = models_open.find_element(By.XPATH,
                                        '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]/div/ul')
        modele = lista_modeli.find_elements(By.TAG_NAME, 'li')
        print(modele)
        for l in modele:
            istotne_modele.append(l.text)
        save_models_to_csv('modele.csv', istotne_modele, marka)



    return istotne_modele





if __name__ == '__main__':
    #marki = read_marki(100)
    #save_to_csv('marki.csv', marki)
    marki_lista = read_from_csv('marki.csv')
    modele = read_models(marki_lista,100)



