class Cat:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age

    def info(self):
        print(f"Кот: {self.name}, порода: {self.breed}, возраст: {self.age} лет")

cat1 = Cat("Британская", "Черчилль", 10)
cat2 = Cat("Сиамская", "Снежок", 2)
cat3 = Cat("Русская обыкновенная", "Мурзик", 5)
cat1.info()
cat2.info()
cat3.info()
