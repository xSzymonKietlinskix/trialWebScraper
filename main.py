import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


def read_from_csv(fileName):
    list = []
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            list.append(row)
    return list


def read_brands(min_amount, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            driver = webdriver.Chrome()
            driver.maximize_window()
            # Otwarcie strony internetowej
            driver.get('https://www.otomoto.pl/osobowe?search%5Badvanced_search_expanded%5D=true')
            # Kliknięcie ciasteczek
            cookies = driver.find_element(By.XPATH,
                                          '//*[@id="onetrust-accept-btn-handler"]')

            cookies.click()

            # kliknij marki (strzałkę)
            brands_open = driver.find_element(By.XPATH,
                                              '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]')

            brands_open.click()
            # pobiera listę marek
            list_brands = driver.find_element(By.XPATH,
                                              '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[1]/div/ul')
            brands = list_brands.find_elements(By.TAG_NAME, 'li')
            valid_brands = []

            for brand in brands:
                l_egz = r'\((.*?)\)'
                if not brand.text == "Wszystkie marki":
                    found = re.search(l_egz, brand.text)
                    if int(found.group(1)) > min_amount:
                        if brand.text == "CitroĂ«n":
                            valid_brands.append("Citroen")
                        else:
                            valid_brands.append(brand.text)

            header = ['brand']
            with open("brands.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for brand in valid_brands:
                    writer.writerow([brand])

            return valid_brands

        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {str(e)}")
            if attempt < max_attempts - 1:
                continue
            else:
                print("Max attempts reached. Exiting.")
                break
        finally:
            if 'driver' in locals() and driver is not None:
                driver.quit()


def read_models(brands, min_amount, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            for brand in brands:
                valid_models = []
                if brand[0] == "brand":
                    continue

                driver = webdriver.Chrome()
                driver.maximize_window()

                brand = brand[0]
                if brand.startswith("Citr"):
                    brand = "Citroen"
                brand = brand.lower()
                brand = re.sub(r'\([^)]*\)', '', brand)
                brand = brand.rstrip()
                brand = brand.replace(" ", "-")
                # Otwarcie strony internetowej
                url = 'https://www.otomoto.pl/osobowe/'
                url += brand
                url += '?search%5Badvanced_search_expanded%5D=true'
                driver.get(url)
                # Kliknięcie ciasteczek
                cookies = driver.find_element(By.XPATH,
                                              '//*[@id="onetrust-accept-btn-handler"]')
                cookies.click()

                models_open = driver.find_element(By.XPATH,
                                                  '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]')
                models_open.click()
                list_models = models_open.find_element(By.XPATH,
                                                       '//*[@id="__next"]/div/div/div/div[2]/div[1]/div/form/section/div/div[2]/div/ul')
                models = list_models.find_elements(By.TAG_NAME, 'li')

                for m in models:
                    if m.text == "Wszystkie modele":
                        continue
                    l_egz = r'\((.*?)\)'
                    found = re.search(l_egz, m.text)
                    if int(found.group(1)) > min_amount:
                        valid_models.append(m.text)

                with open('models.csv', 'a', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    for m in valid_models:
                        if m == "Wszytskie modele":
                            continue
                        row = brand + ';' + m
                        writer.writerow([row])

                driver.quit()

        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {str(e)}")
            if attempt < max_attempts - 1:
                continue
            else:
                print("Max attempts reached. Exiting.")
                break
        finally:
            if 'driver' in locals() and driver is not None:
                driver.quit()


if __name__ == '__main__':
    print("1. Brands \n 2. Models")
    choose = input("Choose number: ")
    if int(choose) == 1:
        brands = read_brands(100, 1)
    elif int(choose) == 2:
        brands_list = read_from_csv('brands.csv')
        read_models(brands_list, 10, 1)
