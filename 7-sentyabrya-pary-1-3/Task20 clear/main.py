class Cart:
    def __init__(self):
        self.goods = []

    def add(self, gd):
        self.goods.append(gd)

    def remove(self, indx):
        del self.goods[indx]

    def get_list(self):
        result = []
        for gd in self.goods:
            result.append(f"{gd.name}: {gd.price}р.")
        return result

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

cart = Cart()
cart.add(TV("Samsung QLED SUPER 8K ULTRA", 500000))
cart.add(TV("LG OLED 4K", 65000))
cart.add(Table("Стол Ardor Gaming", 5000))
cart.add(Notebook("Apple MacBook M67", 120000))
cart.add(Notebook("ASUS TYF A15", 95000))
cart.add(Cup("Кружка Apple", 50000))

for i in cart.get_list():
    print(i)