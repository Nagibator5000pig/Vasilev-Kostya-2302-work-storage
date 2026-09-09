class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

points = [Point(10, 20),
          Point(12, 5, 'red'),
          Point(7, 3, 'green')
          ]

for point in points:
    print(point.x, point.y, point.color)