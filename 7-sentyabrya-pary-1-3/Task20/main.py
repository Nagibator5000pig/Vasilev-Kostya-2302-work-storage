class Table:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class TV:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Notebook:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cup:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.goods = []

    def add(self, gd):
        self.goods.append(gd)

    def remove(self, indx):
        if 0 <= indx < len(self.goods):
            del self.goods[indx]

    def get_list(self):
        return [f"{item.name}: {item.price}р." for item in self.goods]

cart = Cart()

cart.add(TV("Samsung QLED SUPER 8K ULTRA", 50000))
cart.add(TV("LG OLED 4K", 65000))
cart.add(Table("Дубовый стол очень качественный", 15000))
cart.add(Notebook("Apple MacBook M67", 120000))
cart.add(Notebook("ASUS TYF A15", 95000))
cart.add(Cup("Керамическая кружка", 500))

for item in cart.get_list():
    print(item)