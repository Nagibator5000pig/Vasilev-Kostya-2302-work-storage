class Goods:
    title = 'Мороженое'
    weight = 150
    tp = 'Еда'
    price = 100

Goods.price = 2048
setattr(Goods, 'inflation', 100)

print(Goods.price, Goods.inflation)