import json
from person import Person

class PeopleDB:
    def __init__(self):
        self.people = []

    def add(self, person: Person):
        self.people.append(person)

    def search(self, query):
        query = query.lower().strip()
        return [p for p in self.people if query in p.full_name().lower()]

    def save(self, filename):
        data = [p.to_dict() for p in self.people]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.people = [Person.from_dict(p) for p in data]


