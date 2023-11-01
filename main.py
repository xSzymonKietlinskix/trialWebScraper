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

def readWebsite(page):
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup.prettify())
    nadwozia = soup.find_all("div",class_="ooa-1d3w5wq e1kl0nws1")
    #nadwozia = soup.select("div.ooa-1xfqg6o")
    print(f'znalazłem {len(nadwozia)} linków')
    if nadwozia:
        for e in nadwozia:
            print(e.text)

    driver = webdriver.Chrome()
    driver.maximize_window()
    # Otwarcie strony internetowej
    driver.get('https://www.otomoto.pl/osobowe?search%5Badvanced_search_expanded%5D=true')

    button = driver.find_element(By.XPATH,
                                 '//*[@id="onetrust-accept-btn-handler"]')

    # Kliknięcie guzika
    button.click()

    time.sleep(2)

    button = driver.find_element(By.XPATH,
                                 '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]')

    # Kliknięcie guzika
    button.click()
 
    list_marki = driver.find_elements(By.XPATH,
                                '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/ul')
    for l in list_marki:
        checkBox = l.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/ul/li[2]/div/label/input')
        checkBox.click()
        button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/div/span/button')
        button.click()
        button = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]')
        button.click()
        time.sleep(1)
        button = driver.find_element(By.XPATH,
                                     '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]/div/fieldset/span/button')
        button.click()




    for l in list_marki:
        print(l.text)



    driver.quit()





if __name__ == '__main__':
    page = getWebsite()
    readWebsite((page))

