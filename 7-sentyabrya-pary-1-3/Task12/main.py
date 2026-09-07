import sys

class DataBase:
    lst_data = []
    FIELDS = ('id', 'name', 'old', 'salary')

    def insert(self, data):
        for row in data:
            values = row.split()
            record = {}
            for i in range(len(self.FIELDS)):
                record[self.FIELDS[i]] = values[i]
            self.lst_data.append(record)

    def select(self, a, b):
        if b >= len(self.lst_data):
            b = len(self.lst_data) - 1
        return self.lst_data[a:b+1]

lst_in = list(map(str.strip, sys.stdin.readlines()))

db = DataBase()
db.insert(lst_in)

result = db.select(0, len(lst_in) - 1)
print(str(result).replace(' ', ''))