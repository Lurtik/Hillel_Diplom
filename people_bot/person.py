import re
from datetime import date

GENDER_WORDS = {
    "m": {"label": "чоловік", "born": "Народився", "died": "Помер"},
    "f": {"label": "жінка", "born": "Народилася", "died": "Вмерла"},
}

class Person:

    def __init__(self, name, birth, gender, surname="", patronymic = "", death = None):
        if not name.strip():
            raise ValueError("Name is required")

        if gender not in ["m", "f"]:
            raise ValueError("Gender must be 'f' or 'm'")

        if parse_date(birth) > date.today():
            raise ValueError("Birth date must be in the past")

        if death:
            if parse_date(birth) > parse_date(death):
                raise ValueError("Death date must be after birth date")

        self.name = name.strip()
        self.birth = parse_date(birth)
        self.gender = gender
        self.surname = surname.strip()
        self.patronymic = patronymic.strip()
        self.death = parse_date(death) if death else None

    def full_name(self):
        parts = [self.name, self.surname, self.patronymic]
        return " ".join(p for p in parts if p)

    def age(self):
        return calc_age(self.birth, self.death or date.today())

    def __str__(self):
        words = GENDER_WORDS[self.gender]
        age = self.age()
        text = (f"{self.full_name()} {age} {years_word(age)}, {words['label']}. "
                f"{words['born']} {self.birth.strftime('%d.%m.%Y')}.")
        if self.death:
            text += f" {words['died']}: {self.death.strftime('%d.%m.%Y')}."
        return text

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic,
            "birth": self.birth.strftime('%d.%m.%Y'),
            "death": self.death.strftime('%d.%m.%Y') if self.death else None,
            "gender": self.gender,
        }

    @staticmethod
    def from_dict(d):
        return Person(
            name=d["name"],
            birth=d["birth"],
            gender=d["gender"],
            surname=d["surname"],
            patronymic=d["patronymic"],
            death=d["death"] if d["death"] else None,
        )

def parse_date(text):
    parts = re.split(r"[.\s/\-]+", text.strip())
    if len(parts) != 3:
        raise ValueError("Невірний формат дати")
    day, month, year = (int(p) for p in parts)
    return date(year, month, day)

def calc_age(birth, end):
    years = end.year - birth.year
    if (end.month, end.day) < (birth.month, birth.day):
        years -= 1
    return years

def years_word(n):
    if n % 10 == 1 and n % 100 != 11:
        return "рік"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return "роки"
    return "років"

