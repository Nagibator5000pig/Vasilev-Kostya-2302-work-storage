class TriangleChecker:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_triangle(self):
        for x in (self.a, self.b, self.c):
            if not isinstance(x, (int, float)) or x <= 0:
                return 1
        largest_num = max(self.a, self.b, self.c)
        if largest_num >= (self.a + self.b + self.c - largest_num):
            return 2
        return 3

a, b, c = map(int, input().split())
tr = TriangleChecker(a, b, c)
outcome = tr.is_triangle()
print(outcome)

