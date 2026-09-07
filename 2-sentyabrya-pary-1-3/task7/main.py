class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

    def draw(self):
        print("Рисуется фигура")

class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length

    def draw(self):
        print("Рисуется линия...")

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height

    def draw(self):
        print("Рисуется прямоугольник...")

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius

    def draw(self):
        print("Рисуется эллипс...")

fig1 = Figure((0, 0), 10, "красный")
fig2 = Figure((5, 5), 20, "синий")
fig3 = Figure((10, 10), 15, "зелёный")

line = Line((0, 0), 10, "красный", 100)
rect = Rect((5, 5), 20, "синий", 8)
ellipse = Ellipse((10, 10), 15, "зелёный", 7)

print("=== БАЗОВЫЕ ФИГУРЫ (Задача 5) ===")
print(f"Фиг. 1: coords={fig1.coords}, width={fig1.width}, color={fig1.color}")
print(f"Фиг. 2: coords={fig2.coords}, width={fig2.width}, color={fig2.color}")
print(f"Фиг. 3: coords={fig3.coords}, width={fig3.width}, color={fig3.color}")

print("\n=== ДОЧЕРНИЕ ФИГУРЫ (Задача 6) ===")
print(f"Line: coords={line.coords}, width={line.width}, color={line.color}, length={line.length}")
print(f"Rect: coords={rect.coords}, width={rect.width}, color={rect.color}, height={rect.height}")
print(f"Ellipse: coords={ellipse.coords}, width={ellipse.width}, color={ellipse.color}, radius={ellipse.radius}")

print("\n=== РИСУЕМ ФИГУРЫ (Задача 7) ===")
figures = [fig3, line, rect, ellipse]
for figure in figures:
    figure.draw()
