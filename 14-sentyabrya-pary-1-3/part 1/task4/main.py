class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return Point(self.x, self.y)

pt = Point(10, 20)
pt_clone = pt.clone()

print(pt.__dict__)
print(pt_clone.__dict__)
print(pt is pt_clone)