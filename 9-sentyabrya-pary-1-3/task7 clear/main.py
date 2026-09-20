class Graph:
    def __init__(self, data):
        self.data = data.copy()
        self.is_show = True

    def set_data(self, data):
        self.data = data.copy()

    def show_table(self):
        if not self.is_show:
            print('Отображение данных закрыто')
            return
        print(*self.data)

    def show_graph(self):
        if not self.is_show:
            print('Отображение данных закрыто')
            return
        print('Графическое отображение данных:', *self.data)

    def show_bar(self):
        if not self.is_show:
            print('Отображение данных закрыто')
            return
        print('Столбчатая диаграмма:', *self.data)

    def set_show(self, fl_show):
        self.is_show = fl_show

data_graph = list(map(int, input().split()))
gr = Graph(data_graph)
gr.show_bar()
gr.set_show(False)
gr.show_table()
