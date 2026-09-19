import sys
class DataBase:
    lst_data = []
    FIELDS = ('id', 'name', 'old', 'salary')

    def insert(self, data):
        for line in data:
            values = line.split()
            record = {}
            for i in range(len(self.FIELDS)):
                record[self.FIELDS[i]] = values[i]
            self.lst_data.append(record)

    def select(self, a, b):
        return self.lst_data[a:b+1]

lst_in = list(map(str.strip, sys.stdin.readlines()))

db = DataBase()
db.insert(lst_in)
for i in db.select(0, 100):
    print(i)

