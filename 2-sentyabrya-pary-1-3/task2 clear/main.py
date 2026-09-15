class Cat:
    breed = '?'
    name = '?'
    age = '?'

    def draw(self):
        print(f'На экране рисуется кот: {self.name}, порода: {self.breed}')

cat1 = Cat()
cat1.breed = 'Русская'
cat1.name = 'Гоша'
cat1.age = 8

cat2 = Cat()
cat2.breed = 'Русская голубая'
cat2.name = 'Ромка'
cat2.age = 5

cat3 = Cat()
cat3.breed = 'Бомбейская'
cat3.name = 'Дед'
cat3.age = 15

for cat in (cat1, cat2, cat3):
    print(f'Имя: {cat.name}, Порода: {cat.breed}, возраст: {cat.age}')
    cat.draw()