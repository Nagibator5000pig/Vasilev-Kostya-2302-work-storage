TYPE_OS = 1

class DialogWindows:
    name_class = 'DialogWindows'
    def __init__(self, name):
        self.name = name

class DialogLinux:
    name_class = 'DialogLinux'
    def __init__(self, name):
        self.name = name

class Dialog:
    def __new__(cls, *args, **kwargs):
        if TYPE_OS == 1:
            return DialogWindows(*args, **kwargs)
        return DialogLinux(*args, **kwargs)

d1g = Dialog('Настройки')
print(type(d1g).__name__)
print(d1g.name)
print()

TYPE_OS = 2

d1g = Dialog('Настройки')
print(type(d1g).__name__)
print(d1g.name)