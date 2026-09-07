class Graph:
    def __init__(self, x=0, y=0, scale=1.0):
        self._x = x
        self._y = y
        self._scale = scale

    def move(self, dx, dy):
        self._x += dx
        self._y += dy
        print(f"График перемещён на ({dx}, {dy})")

    def change_scale(self, factor):
        self._scale *= factor
        print(f"Масштаб изменён в {factor} раз")

    def get_state(self):
        return f"x={self._x}, y={self._y}, scale={self._scale}"


graph1 = Graph()
graph2 = Graph(5, 10, 2.0)
graph3 = Graph(-3, 7, 0.5)

graphs = [graph1, graph2, graph3]

def get_number(prompt, error_message="Введите число!"):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error_message)

while True:
    print("\n=== СПИСОК ГРАФИКОВ ===")
    for i, g in enumerate(graphs):
        print(f"{i+1}. {g.get_state()}")
    print("4. Выйти из программы")

    choice = input("Выберите номер графика для изменения (1-3) или 4 для выхода: ").strip()

    if choice == "4":
        print("До свидания!")
        break

    if choice not in ["1", "2", "3"]:
        print("Неверный выбор! Введите число от 1 до 4.")
        continue

    idx = int(choice) - 1
    selected = graphs[idx]

    while True:
        print(f"\nВыбран график {choice}: {selected.get_state()}")
        print("Что хотите сделать?")
        print("1. Переместить график")
        print("2. Изменить масштаб")
        print("3. Оставить как есть (ничего не делать)")
        print("4. Вернуться к выбору графика")

        action = input("Выберите действие (1-4): ").strip()

        if action == "1":
            dx = get_number("Введите dx (смещение по X): ")
            dy = get_number("Введите dy (смещение по Y): ")
            selected.move(dx, dy)
            print(f"Текущее состояние: {selected.get_state()}")
            break

        elif action == "2":
            factor = get_number("Введите коэффициент изменения масштаба: ")
            if factor <= 0:
                print("Масштаб должен быть положительным числом! Попробуйте снова.")
                continue
            selected.change_scale(factor)
            print(f"Текущее состояние: {selected.get_state()}")
            break

        elif action == "3":
            print("График оставлен без изменений.")
            break

        elif action == "4":
            break

        else:
            print("Неверный выбор! Введите число от 1 до 4.")
