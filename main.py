import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
import csv
def getWebsite():
    url = "https://www.otomoto.pl/"
    try:
        response = requests.get(url)
        response.raise_for_status()

        #print("Zawartość strony: \n")
        #print(response.text)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas wykonywania żądania: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Błąd http: {e}")
        return None

#czytanie stony
def readWebsite(page):


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
    for marka in marki:
        print(marka.text)
        if not marka.text == "Wszystkie marki":
            test = marka.find_element(By.TAG_NAME, 'input')
            time.sleep(1)
            if not test.is_selected():
                test.click()

    # for marka in marki:
    #
    #     print(marka.text)
    #     select_marka = marka.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/ul/li[2]/div/label/input')
    #     select_marka.click()
    #     brands_close = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/div/span/button')
    #     brands_close.click()
    #     models_open = driver.find_element(By.XPATH,
    #                                    '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]')
    #     models_open.click()
    #
    #     lista_modeli = models_open.find_elements(By.XPATH,
    #                                  '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]/div/ul')
    #     for model in lista_modeli:
    #         print(model.text)
    #
    #     models_close = driver.find_element(By.XPATH,
    #                                        '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]/div/fieldset/span/button')
    #     models_close.click()
    #
    #     time.sleep(2)
    #
    #     brand_cancel = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/div/span/button')
    #     brand_cancel.click()
    #     time.sleep(2)
    #     brands_open2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/div/span/button')
    #     brands_open2.click()







    driver.quit()





if __name__ == '__main__':
    page = getWebsite()
    readWebsite((page))

