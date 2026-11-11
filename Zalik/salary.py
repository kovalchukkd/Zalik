#Файл з виконанням другого сценарію
import csv
from pathlib import Path

import pclasses

OUTPUT = Path(__file__).parent / "output" / "salaries.csv"

def buildschool() -> pclasses.School:
    #Створює школу та додає працівників
    school = pclasses.School("Школа")
    school.addemployee(pclasses.Director("Йосип", "Іваненко", "Петрович", 15000, texperience = 25, mexperience = 10))
    school.addemployee(pclasses.Teacher("Марія", "Іваненко", "Володимірівна", 12000, texperience = 20))
    school.addemployee(pclasses.Teacher("Андрій", "Ковальов", "Сергійович", 12000, texperience = 10))
    school.addemployee(pclasses.Teacher("Олена", "Кац", "Іванівна", 12000, texperience = 30))
    school.addemployee(pclasses.Guard("Василь", "Іваненко", "Йосипович", 11000, gexperience = 25))
    return school

def salaryrows(employees : list[pclasses.Employee]) -> list[dict[str, str | float]]:
    #Викликає calculate для всіх працівників
    return [{"ПІБ" : e.fullname, "Посада" : e.position, "Базова ставка" : e.baserate, "Зарплата" : round(e.calculate(), 2)} for e in employees]

def save(rows : list[dict[str, str | float]], path : Path) -> None:
    #Зберігає зарплати в csv
    path.parent.mkdir(parents = True, exist_ok = True)
    with open(path, "w", encoding = "utf-8-sig", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main() -> None:
    school = buildschool()
    rows = salaryrows(school.employees)
    print(f"{'ПІБ':<32}{'Посада':<12}{'Ставка':>10}{'Зарплата':>12}")
    print("-" * 66)
    for r in rows:
        print(f"{r['ПІБ']:<32}{r['Посада']:<12}{r['Базова ставка']:>10.0f}{r['Зарплата']:>12.2f}")
    print("-" * 66)
    print(f"{'Разом':<54}{sum(r['Зарплата'] for r in rows):>12.2f}")
    save(rows, OUTPUT)
    print(f"\nТаблицю збережено: {OUTPUT}")

if __name__ == "__main__":
    main()

