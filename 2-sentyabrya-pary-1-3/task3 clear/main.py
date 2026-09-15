class Car:
    _engine_temperature = 20

    def start_engine(self):
        self._engine_temperature = 90

    def drive(self):
        if self._engine_temperature >= 90:
            print('Поехали!')
        else:
            print('Двигатель прогрет недостаточно. Для начала поездки необходимо прогреть двигатель.')

car = Car()
car.drive()
car.start_engine()
car.drive()

#car._engine_temperature = 90
#car.drive()
