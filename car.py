import csv
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.generation = "none"

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


