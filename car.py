import csv
import re
class Car:
    def __init__(self, brand, model, generation="none"):
        self.brand = brand
        self.model = model
        self.generation = generation

    def create_car_list(fileName):
        car_list = []
        with open(fileName, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) != 0:
                    brand, model = row
                    car = Car(brand, model)
                    car_list.append(car)
        return car_list


    def create_car_list_gen(fileName):
        car_list = []
        with open(fileName, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) != 0:
                    brand, model, generation = row
                    model = model.lower()
                    model = re.sub(r'\([^)]*\)', '', model)
                    model = model.rstrip()
                    model = model.replace(" ", "-")
                    generation = generation.lower()
                    generation = re.sub(r'\([^)]*\)', '', generation)
                    generation = generation.rstrip()
                    generation = generation.replace(" ", "-")
                    car = Car(brand, model, generation)
                    car_list.append(car)
        return car_list