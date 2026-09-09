class Goods:
    title = "Мороженое"
    weight = 150
    type = "Еда"
    price = 100

setattr(Goods, "price", 2048)
setattr(Goods, "inflation", 100)
attrs = ["title", "weight", "type", "price", "inflation"]
obj = Goods()

for attr in attrs:
    print(getattr(obj, attr))