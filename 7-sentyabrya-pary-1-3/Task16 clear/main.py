import random

class Line:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Rect:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Ellipse:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

elements = []

for i in range(217):
    fig = random.choice([Line, Rect, Ellipse])
    obj = fig(random.randint(-99, 99), random.randint(-99, 99),
               random.randint(-99, 99),random.randint(-99, 99))
    elements.append(obj)

for i in elements:
    if isinstance(i, Line):
        i.sp = (0, 0)
        i.ep = (0, 0)

for el in elements:
    print(type(el).__name__, el.__dict__)

