class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

p1 = Point(10, 20)
p2 = Point(12, 5, 'red')

points = []

for i in range(1, 2000, 2):
    p = Point(i, i)
    points.append(p)

points[1].color = 'yellow'

for i in points:
    print(i.__dict__)


