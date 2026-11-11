#Файл для генерації csv файлів

import csv
import random
from pathlib import Path

random.seed(67)
DATA = Path(__file__).parent /"data"
DATA.mkdir(exist_ok = True)

MID = ["Коваленко", "Ковальчук", "Шевченко", "Сталін", "Бондаренко", "Шваб","Мельник", "Ткаченко", "Кравченко", "Олійник",
        "Савченко", "Петренко", "Мороз", "Фелінгхер", "Лисенко", "Гончар", "Поліщук", "Руденко", "Бойко", "Маркс", "Штірнер", "Енгельс", "Ранд"]
MNAME = ["Андрій", "Клаус", "Олександр", "Максим", "Йосип", "Гюнтер", "Іван", "Дмитро", "Богдан", "Назар", "Артем", "Карл"]
FNAME = ["Марія", "Анна", "Айн", "Емма", "Мелісса", "Софія", "Олена", "Дарина", "Юлія", "Катерина", "Вікторія", "Ксенія"]
XNAME = ["Еш", "Онікс", "Лейк", "Рівер", "Кат", "Стоун", "Анаг", "Фелікс"]
LAST_M = ["Андрійович", "Олександрович", "Іванович", "Петрович", "Сергійович"]
LAST_F = ["Андріївна", "Олександрівна", "Іванівна", "Петрівна", "Сергіївна"]
LETTERS = ["А", "Б", "В", "Г"]
FIRST_GRADE_BIRTH = 2020

with open(DATA /  "classes.csv", "w", encoding = "utf-8", newline = "") as cf, \
    open(DATA / "students.csv", "w", encoding= "utf-8", newline = "") as sf:
    cw, sw = csv.writer(cf), csv.writer(sf)
    cw.writerow(["classid", "grade", "letter"])
    sw.writerow(["classid", "firstname", "midname", "lastname", "birthyear", "sex", "avggrade"])
    cid = 0
    for grade in range(1, 12):
        for letter in LETTERS[:random.randint(2,4)]: #Створення класів
            cid += 1
            cw.writerow([cid, grade, letter])
            for _ in range(random.randint(15, 45)):
                m = random.random() < 0.5
                f = random. random() < 0.5
                birth = FIRST_GRADE_BIRTH - (grade - 1) - random.choice([0, 0, 0, 1])
                sw.writerow([cid, random.choice(MNAME if m else (FNAME if f else XNAME)), random.choice(MID),
                             random.choice(LAST_M if m else (LAST_F if f else (LAST_M + LAST_F))), 
                             birth, "M" if m else("F" if f else "X"), round(random.uniform(5.5, 12), 1)])
print("Ready:", DATA)
