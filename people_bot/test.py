from database import PeopleDB
from person import Person

db = PeopleDB()
db.add(Person("Євген", "12.10.1980", "m", "Крут", "Михайлович", "11.10.2001"))
db.add(Person("Євгенія", "12.10.1980", "f", death="12.10.2001"))
db.add(Person("Дмитро", "10.03.2000", "m", patronymic="Євгенович"))

print(len(db.people))

print(len(db.search("євген")))        # должно быть 3
print(len(db.search("євген крут")))   # должно быть 1
print(len(db.search("ЄВГЕН")))        # должно быть 3
print(len(db.search("xyz")))          # должно быть 0

db.save("test.json")

db2 = PeopleDB()
print(len(db2.people))      # 0, это новая пустая коробка
db2.load("test.json")
print(len(db2.people))      # 3

for p in db2.search("євген"):
    print(p)