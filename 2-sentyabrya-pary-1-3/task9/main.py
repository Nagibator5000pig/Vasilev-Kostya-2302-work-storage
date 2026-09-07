import math

class Figure:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coords(self):
        return (self._x, self._y)

    def set_coords(self, x, y):
        self._x = x
        self._y = y

    def calculate_area(self):
        return 0

class Circle(Figure):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def calculate_area(self):
        return math.pi * self.radius ** 2

class Square(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.side = side

    def calculate_area(self):
        return self.side ** 2

def get_number(prompt, error_message="Введите число!"):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error_message)

figures = []

while True:
    print("\n=== МИНИ-ГРАФИЧЕСКИЙ РЕДАКТОР ===")
    print("1. Создать круг (Circle)")
    print("2. Создать квадрат (Square)")
    print("3. Показать все фигуры")
    print("4. Посчитать общую площадь всех фигур")
    print("5. Выйти")

    choice = input("Выберите действие (1-5): ").strip()

    if choice == "1":
        x = get_number("Введите x: ")
        y = get_number("Введите y: ")
        radius = get_number("Введите радиус: ")
        if radius <= 0:
            print("Радиус должен быть положительным!")
            continue
        figures.append(Circle(x, y, radius))
        print(f"Круг с радиусом {radius} создан!")

    elif choice == "2":
        x = get_number("Введите x: ")
        y = get_number("Введите y: ")
        side = get_number("Введите сторону: ")
        if side <= 0:
            print("Сторона должна быть положительной!")
            continue
        figures.append(Square(x, y, side))
        print(f"Квадрат со стороной {side} создан!")

    elif choice == "3":
        if len(figures) == 0:
            print("Фигур пока нет! Создайте хотя бы одну.")
        else:
            print("\n=== СПИСОК ФИГУР ===")
            for i, fig in enumerate(figures):
                coords = fig.get_coords()
                if isinstance(fig, Circle):
                    print(f"{i+1}. Круг: coords={coords}, radius={fig.radius}, area={fig.calculate_area():.2f}")
                elif isinstance(fig, Square):
                    print(f"{i+1}. Квадрат: coords={coords}, side={fig.side}, area={fig.calculate_area():.2f}")

    elif choice == "4":
        if len(figures) == 0:
            print("Нет фигур для подсчёта! Создайте хотя бы одну.")
        else:
            total_area = 0
            for fig in figures:
                total_area += fig.calculate_area()
            print(f"\nОбщая площадь всех фигур: {total_area:.2f}")

    elif choice == "5":
        print("До свидания!")
        break

    else:
        print("Неверный выбор! Попробуйте снова.")
