class Figure:
    coords = (0,0)
    width = 1
    color = 'Оранжевый'

class Line(Figure):
    length = 0

class Rect(Figure):
    height = 0

class Ellipse(Figure):
    radius = 0

line1 = Line()
line1.length = 10

rect1 = Rect()
rect1.height = 15

ell1 = Ellipse()
ell1.radius = 6

for figname, f in (('line1', line1), ('rect1',rect1), ('ell1',ell1)):
    print(f'Фигура {figname}, координаты: {f.coords}, ширина: {f.width}, цвет: {f.color}', end='')
    if hasattr(f,'length'):
        print(f', длина = {f.length}', end='')
    if hasattr(f,'height'):
        print(f', высота = {f.height}', end='')
    if hasattr(f,'radius'):
        print(f', радиус = {f.radius}', end='')
    print()




