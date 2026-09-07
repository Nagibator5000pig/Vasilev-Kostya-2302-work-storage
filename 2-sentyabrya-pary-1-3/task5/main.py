class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

print("=" * 3 + "Базовый класс Figure с общими свойствами:" + "=" * 3)

print("coords - кортеж координат (x, y)")
print("width - ширина")
print("color - цвет")

fig1 = Figure((0, 0), 10, "красный")
fig2 = Figure((5, 5), 20, "синий")
fig3 = Figure((10, 10), 15, "зелёный")

print("\nСозданы три фигуры:")
print(f"Фиг. 1: coords={fig1.coords}, width={fig1.width}, color={fig1.color}")
print(f"Фиг. 2: coords={fig2.coords}, width={fig2.width}, color={fig2.color}")
print(f"Фиг. 3: coords={fig3.coords}, width={fig3.width}, color={fig3.color}")
