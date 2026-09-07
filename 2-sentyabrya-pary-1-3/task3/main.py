class Car:
    def __init__(self):
        self._engine_temperature = 20

    def start_engine(self):
        self._engine_temperature = 90
        print("Двигатель прогрет")

    def drive(self):
        if self._engine_temperature >= 90:
            print("Поехали!")
        else:
            print("Двигатель холодный! Запустите start_engine()")

my_car = Car()

while True:
    print("\n=== УПРАВЛЕНИЕ АВТОМОБИЛЕМ ===")
    print(f"Температура двигателя: {my_car._engine_temperature}°C")
    print("1. Завести двигатель")
    print("2. Поехать")
    print("3. Посмотреть температуру (прямой доступ к _engine_temperature)")
    print("4. Выйти")

    choice = input("Выберите действие (1-4): ")

    if choice == "1":
        my_car.start_engine()

    elif choice == "2":
        my_car.drive()

    elif choice == "3":
        print(f"Температура двигателя: {my_car._engine_temperature}°C")

    elif choice == "4":
        print("Закрываюсь...")
        break

    else:
        print("Что-то ты не то пишешь! Попробуйте снова.")
