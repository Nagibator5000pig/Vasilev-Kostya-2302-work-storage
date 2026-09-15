import math
class Figure:
    _coords = (0,0)

    def get_coords(self):
        return self._coords

    def set_coords(self, coords):
        self._coords = coords

class Circle(Figure):
    radius = 0

    def calculate_area(self):
        return math.pi * self.radius ** 2

class Square(Figure):
    side = 0

    def calculate_area(self):
        return self.side ** 2

c1 = Circle()
c1.radius = 2
c1.set_coords((0, 0))

c2 = Circle()
c2.radius = 3
c2.set_coords((5, 5))

s1 = Square()
s1.side = 4
s1.set_coords((2, 2))

s2 = Square()
s2.side = 6
s2.set_coords((7, 7))

s3 = Square()
s3.side = 10
s3.set_coords((10,10))

figures = [c1, c2, s1, s2, s3]
total_area = 0

for f in figures:
    total_area += f.calculate_area()
print(f"Общая площадь всех фигур: {total_area}")


