#Файл для зчитування даних з .csv файлів в об'єкти класів

import csv
from pathlib import Path
from typing import TextIO
import pclasses

def loadstatsfromcsv(classes_file: TextIO, students_file: TextIO, name: str = "Школа") -> pclasses.School:
    #Завантажує статистику школи з двох .csv файлів
    school = pclasses.School(name)
    byid : dict[str, pclasses.Year] = {}

    for row in csv.DictReader(classes_file):
        year = pclasses.Year(grade = int(row["grade"]), letter = str(row["letter"]).strip()) #Створює об'єкт pslasses.Year для кожного класу в таблиці
        byid[row["classid"]] = year 
        school.addgroup(year) 

    for idx, row in enumerate(csv.DictReader(students_file), start = 1):
        student = pclasses.Student(firstname = row["firstname"], midname= row["midname"], lastname= row["lastname"], #Створює об'єкт pclasses.Student для кожного учня в таблиці
                                   birthyear=int(row["birthyear"]), sex = row["sex"].strip(), 
                                   avggrade= float(row["avggrade"]), id= idx
                                   )
        byid[row["classid"]].addstudent(student)

    return school

def loadschool(classp : Path, studentp : Path, name : str = "Школа") -> pclasses.School:
    #Завантажує школу з файлів на диску
    with open(classp, encoding= "utf-8-sig", newline="") as cf, \
        open(studentp, encoding = "utf-8-sig", newline = "") as sf:
        return loadstatsfromcsv(cf,sf, name)






