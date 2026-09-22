class SingletonFive:
    __count = 0
    __last = None

    def __new__(cls, *args, **kwargs):
        if cls.__count < 5:
            obj = super().__new__(cls)
            cls.__count += 1
            cls.__last = obj
            return obj
        return cls.__last

    def __init__(self, name):
        if not hasattr(self, 'name'):
            self.name = name

objs = [SingletonFive(str(n)) for n in range(10)]

for o in objs:
    print(id(o), o.name)