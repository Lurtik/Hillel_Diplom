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
        ...

    def load(self, filename):
        ...


