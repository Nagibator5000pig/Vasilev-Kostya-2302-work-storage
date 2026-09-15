class Graph:
    _x = 0
    _y = 0
    _scale = 1.0

    def move(self, x, y):
        self._x += x
        self._y += y

    def change_scale(self, factor):
        self._scale *= factor

g1 = Graph()
g1.move(5, 10)
g2 = Graph()
g2.change_scale(5)
g3 = Graph()

for figname, g in (('g1', g1), ('g2', g2), ('g3', g3)):
    print(f'График: {figname} x = {g._x}, y = {g._y}, масштаб = {g._scale}')



