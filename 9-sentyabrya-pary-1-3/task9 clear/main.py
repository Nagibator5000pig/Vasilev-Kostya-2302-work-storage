class Figure:
    coords = (0, 0)
    width = 1
    color = 'black'

    def draw(self):
        print('Рисуется фигура')

class Line(Figure):
    def draw(self):
        print('Рисуется линия')

class Rect(Figure):
    def draw(self):
        print('Рисуется прямоугольник')

class Ellipse(Figure):
    def draw(self):
        print('Рисуется эллипс')

class Triangle(Figure):
    def draw(self):
        print('Рисуется треугольник')

line1 = Line()
rect1 = Rect()
ell1 = Ellipse()
tr1 = Triangle()

lst = [line1, rect1, ell1, tr1]

for i in lst:
    i.draw()