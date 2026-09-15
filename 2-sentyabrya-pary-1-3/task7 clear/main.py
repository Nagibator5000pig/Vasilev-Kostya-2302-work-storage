class Figure:
    coords = (0,0)
    width = 1
    color = 'Оранжевый'

    def draw(self):
        print('Рисуется фигура...')

class Line(Figure):
    length = 0

    def draw(self):
        print('Рисуется линия')

class Rect(Figure):
    height = 0

    def draw(self):
        print('Рисуется прямоугольник')

class Ellipse(Figure):
    radius = 0

    def draw(self):
        print('Рисуется эллипс')

line1 = Line()
line1.length = 10

rect1 = Rect()
rect1.height = 15

ell1 = Ellipse()
ell1.radius = 6

figures = [line1, rect1, ell1]
for f in figures:
    print(f'Фигура: координаты: {f.coords}, ширина: {f.width}, цвет: {f.color}', end='')
    if hasattr(f,'length'):
        print(f', длина = {f.length}', end='')
    if hasattr(f,'height'):
        print(f', высота = {f.height}', end='')
    if hasattr(f,'radius'):
        print(f', радиус = {f.radius}', end='')
    print()
    f.draw()



