class Money:
    def __init__(self, amount):
        self.money = amount

my_money = Money(100)
your_money = Money(1000)

lst = (my_money, your_money)

for i in lst:
    print(i.__dict__)