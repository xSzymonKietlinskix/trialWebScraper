import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from car import Car


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


def read_models(brands, min_amount, max_attempts=3, start_from_brand="none"):
    for attempt in range(max_attempts):
        try:
            for brand in brands:
                valid_models = []
                if brand[0] == "brand":
                    continue

                brand = brand[0]
                if brand.startswith("Citr"):
                    brand = "Citroen"
                brand = brand.lower()
                brand = re.sub(r'\([^)]*\)', '', brand)
                brand = brand.rstrip()
                brand = brand.replace(" ", "-")
                if start_from_brand != "none":
                    if brand != start_from_brand:
                        continue
                    else:
                        start_from_brand = "none"

                driver = webdriver.Chrome()
                driver.maximize_window()
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
                    if m.text.startswith("W124"):
                        valid_models.append("W124 (100)")
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


def read_generations(cars, min_amount=5, max_attempts=3, start_from_brand="none"):
    for attempt in range(max_attempts):
        try:
            for car in cars:

                brand = car.brand
                if start_from_brand != "none":
                    if brand != start_from_brand:
                        continue
                    else:
                        start_from_brand = "none"
                model = car.model

                model = model.lower()
                model = re.sub(r'\([^)]*\)', '', model)
                model = model.rstrip()
                model = model.replace(" ", "-")
                if model == 'inny':
                    continue
                # Otwarcie strony internetowej
                driver = webdriver.Chrome()
                driver.maximize_window()

                url = 'https://www.otomoto.pl/osobowe/'
                url += brand + "/" + model
                url += '?search%5Badvanced_search_expanded%5D=true'
                driver.get(url)
                # Kliknięcie ciasteczek
                try:
                    cookies = driver.find_element(By.XPATH,
                                              '//*[@id="onetrust-accept-btn-handler"]')
                    cookies.click()
                except Exception as e:
                    if driver is not None:
                        driver.quit()
                    continue

                try:
                    generations_open = driver.find_element(By.XPATH,
                                                           '/html/body/div[1]/div/div/div/div[2]/div[1]/div/form/section/div/div[3]/div/fieldset')
                    generations_open.click()
                    list_generations = driver.find_element(By.XPATH,
                                                           '/html/body/div[1]/div/div/div/div[2]/div[1]/div/form/section/div/div[3]/div/ul')
                    if list_generations is not None:
                        generations = list_generations.find_elements(By.TAG_NAME, 'li')
                        for g in generations:
                            if g.text == "Wszystkie generacje":
                                continue
                            # l_egz = r'\((.*?)\)'
                            # found = re.search(l_egz, g.text)
                            # if int(found.group(1)) > min_amount:
                            with open('generations.csv', 'a', encoding='UTF8', newline='') as f:
                                writer = csv.writer(f)
                                row = car.brand + ';' + car.model + ';' + g.text
                                writer.writerow([row])



                except Exception as e:
                    if driver is not None:
                        driver.quit()
                    with open('generations.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        row = car.brand + ';' + car.model + ';' + 'none'
                        writer.writerow([row])
                    continue

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
    print("1. Brands \n 2. Models \n 3. Generations \n 4. Models, start from brand xyz")
    choose = input("Choose number: ")
    if int(choose) == 1:
        brands = read_brands(100, 1)
    elif int(choose) == 2:
        brands_list = read_from_csv('brands.csv')
        read_models(brands_list, 20, 1)
    elif int(choose) == 3:
        cars = Car.create_car_list('models.csv')
        read_generations(cars, 5, 1, 'dacia')
    elif int(choose) == 4:
        print("Currently not available")
        # brands_list = read_from_csv('brands.csv')
        # read_models(brands_list, 10, 1, "mini")
