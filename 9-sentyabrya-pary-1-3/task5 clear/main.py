class Point:
    def __init__(self, x, y, color = 'black'):
        self.x = x
        self.y = y
        self.color = color

p1 = Point(10, 20)
p2 = Point(12, 5, 'red')
p3 = Point(15, 20, 'blue')

for i in (p1, p2, p3):
    print(i.__dict__)
