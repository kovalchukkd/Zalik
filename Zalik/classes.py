#Файл з класами проєкту
from collections import defaultdict
from email.policy import default
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from time import strftime

class Sex(str, Enum): #Змінна типу Enum для маркерів статі, має три можливі значення: М(чоловіча), F(жіноча), X(невизначена/небінарні)
    MALE = "M"
    FEMALE = "F"
    NONBINARY = "X"

@dataclass
class Person(ABC):
    #Базовий клас для всіх людей в школі
    firstname : str #Ім'я
    midname : str #Прізвише
    lastname : str #По батькові

    @property
    def fullname(self) -> str:
        return f"{self.midname} {self.firstname} {self.lastname}" #Прізвище Ім'я По батькові

@dataclass
class Student(Person):
    #Клас студента, наслідує клас Person
    birthyear : int
    sex : Sex
    avggrade : float
    id : int = 0 #Унікальний індентифікатор кожного студента

@dataclass
class Year:
    #Клас для класів в яких навчаються учні
    grade : int
    letter : str
    students : list[Student] = field(default_factory=list)

    @property
    def yearname(self) -> str:
        return f"{self.grade}{self.letter}"

    @property
    def size(self) -> int:
        return len(self.students)

    @property
    def avggrade(self) ->int:
        return sum(s.avggrade for s in self.students) / self.size if self.students else 0.0

    def addstudent(self, student: Student) -> None:
        self.students.append(student)

    def promote(self) -> bool:
        #Переводить на наступний рік студентів, повертає False якщо студенти в 11 класі і їх треба ліквідувати

        if self.grade == 11:
            return False
        self.grade += 1
        return True

@dataclass
class Employee(Person, ABC):
    #Абстрактний клас для працівників школи
    position : str = "Працівник"

    def __init__(self, firstname : str, midname : str, lastname : str, baserate : float):
        super().__init__(firstname, midname, lastname)
        self.baserate : float = baserate

    @abstractmethod
    def calculate(self) -> float:
        return 0
        #Метод для обчислення зарплати працівника(Розраховується в нащадках)

class Director(Employee):
    position = "Директор"

    def __init__(self, firstname : str, midname : str, lastname : str, baserate : float, texperience : int, mexperience : int):
        super().__init__(firstname, midname, lastname, baserate)
        self.texperience : int = texperience #texperience - Стаж роботи вчителем
        self.mexperience :int = mexperience #mexperience - Стаж роботи директором
       
    def calculate(self) -> float:
        return self.baserate * self.texperience / 50 + self.mexperience * 500

class Teacher(Employee):
    position = "Вчитель"

    def __init__(self, firstname : str, midname : str, lastname : str, baserate : float, texperience : int):
        super().__init__(firstname, midname, lastname, baserate)
        self.texperience : int = texperience #texperience - Стаж роботи вчителем

    def calculate(self) -> float:
        return self.baserate * self.texperience / 30

class Guard(Employee):
    position = "Охоронець"

    def __init__(self, firstname : str, midname : str, lastname : str, baserate : float, gexperience : int):
        super().__init__(firstname, midname, lastname, baserate)
        self.gexperience : int = gexperience #gexperience - Стаж роботи охоронцем

    def calculate(self) -> float:
        return self.baserate + self.gexperience * 250

@dataclass
class SchoolStats:
    #Клас для статистики школи(Використовується в getstats)
    totalstudents : int #Загална кілкість учнів
    mpercent : float #Процент учнів за статтю
    fpercent : float
    xpercent : float
    studperclass : float #Середня кількість студентів в класі
    maxstud : Year | None #Класи з найбільшою/найменшою кількістю студентів
    minstud : Year | None

class School:
    #Клас школи
    def __init__(self, name : str):
        self.name : str = name
        self.groups: list[Year] = []
        self.employees: list[Employee] = []

    def addgroup(self, newyear : Year) -> None:
        self.groups.append(newyear)

    def addemployee(self, newempolyee : Employee) -> None:
        self.employees.append(newempolyee)

    #Статистика
    def allstudents(self) -> list[Student]:
        return [s for c in self.groups for s in c.students]

    def getstats(self) -> SchoolStats:
        students = self.allstudents
        total = len(students)
        males = sum(1 for s in students if s.sex == Sex.MALE)
        females = sum(1 for s in students if s.sex == Sex.FEMALE)
        nonempty = self.groups
        return SchoolStats(totalstudents = total,
                           mpercent= males / total * 100 if total else 0.0,
                           fpercent= females / total * 100 if total else 0.0,
                           xpercent= (total - males - females) / total * 100 if total else 0.0,
                           studperclass= total / len(nonempty) if nonempty else 0.0,
                           maxstud = max(nonempty, key = lambda c: c.size, default = None),
                           minstud= min(nonempty, key = lambda c: c.size, default = None))

    def studpergrade(self) -> dict[int, int]:
        result: dict[int, int] = defaultdict(int)
        for c in self.groups:
            result[c.grade] += c.size
        return dict(sorted(result.items()))

    def studperletter(self) -> dict[str, float]:
        sizes: dict[str, list[int]] = defaultdict[list]
        for c in self.groups:
            sizes[c.letter].append(c.size)
        return {k: sum(v) / len(v) for k, v in sorted(sizes.items())}

    def studbybirthyear(self) -> dict[int, int]:
        result: dict[int, int] = defaultdict(int)
        for s in self.allstudents:
            result[s.birthyear] += 1
        return dict(sorted(result.items()))

    #Переведення
    def promoteall(self) -> list[Student]:
        graduated : list[Student] = []
        remaining : list[Year] = []
        for c in self.groups:
            if c.promoteall():
                remaining.append(c)
            else:
                graduated.extend(c.students)
        self.groups = remaining
        return graduated


