#Файл з виконанням першого сценарія на streamlit

from pathlib import Path
import streamlit as st
import io
import copy
import pclasses
import dataloader

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(page_title = "Статистика школи", layout = "wide")

def renderstats(school: pclasses.School) -> None:
    #Виводить текстову статистику школи
    stats = school.getstats()
    c1, c2, c3 = st.columns(3)
    c1.metric("Загальна кількість учнів", stats.totalstudents)
    c2.metric("Співвідношення учнів за статтю", f"M : {stats.mpercent : .1f} %, F : {stats.fpercent : .1f} %, X : {stats.xpercent : .1f} %")
    c3.metric("Середня кількість учнів на клас: ", f"stats.studperclass : .1f")

    c4, c5 = st.columns(2)
    if stats.maxstud:
        c4.metric("Клас з найбільшою кількістю студентів: ", f"{stats.maxstud} {stats.maxstud.yearname}")
    if stats.minstud:
        c4.metric("Клас з найменшою кількістю студентів: ", f"{stats.minstud} {stats.minstud.yearname}")

def rendercharts(school : pclasses.School) -> None:
    #Стовпчикові діаграми
    col1, col2 = st.columns(2)

    col1.subheader("Учні по паралелях")
    bygrade = school.studpergrade()
    col1.bar_chart({"Паралель": list(bygrade), "Учнів" : list(bygrade.values())}, x = "Паралель", y = "Учнів")

    col2.subheader("Сер. кількість учнів на вертикаль")
    byletter = school.studperletter
    col2.bar_chart({"Паралель": list(byletter), "Учнів" : list(byletter.values())}, x = "Вертикаль", y = "Сер. кількість учнів")

    col3, col4 = st.columns(2)
    #Лінійний графік
    col3.subheader("Кількість учнів за роком народження")
    bybirth = school.studbybirthyear
    col3.line_chart({"Рік народження": list(byletter), "Учнів" : list(byletter.values())}, x = "Рік народження", y = "Учнів")
    #Графік залежності scatter
    col4.subheader("Залежність середньої оцінки від класу школу")
    pairz = [(c.grade, s.avggrade, c.letter) for c in school.groups for s in school.students]
    col4.scatter_chart({"Клас (паралель)" : [p[0] for p in pairz],
                        "Середня оцінка" : [p[1] for p in pairz],
                        "Клас (вертикаль)" : [p[2] for p in pairz]}, x="Клас(паралель)", y = "Середня оцінка", color = "Клас(вертикаль)")

def renderschool(school : pclasses.School) -> None:
    #Виликає попередні функції та виводить табличечку з класами
    renderstats(school)
    st.subheader("Графіки")
    rendercharts(school)
    st.datagrame([{"Клас" : c.name, "Паралель" : c.grade, "Вертикаль" : c.letter, "Учнів" : c.size, "Сер. Оцінка" : round(c.avggrade, 2)}
                  for c in sorted(school.groups, key = lambda c: (c.grade, c.letter))], use_container_width = True, hide_index = True)
    st.caption("Якщо файл не завантажено, використовується таблиця з /data")

#Створення сторінки веб додатка
st.title("Статистика учнів школи")

with st.sidebar:
    st.header("Дані")
    upclasses = st.file_uploader("classes.csv", type="csv")
    upstuds = st.file_uploader("students.csv", type="csv")

    if upclasses and upstuds :
        original = dataloader.loadstatsfromcsv(
            io.TextIOWrapper(upclasses, encoding= "utf-8-sig", newline=""),
            io.TextIOWrapper(upstuds, encoding= "utf-8-sig", newline=""), "Моя школа")

    else:
        original = dataloader.loadschool(DATA_DIR / "classes.csv", DATA_DIR / "students.csv", "Моя школа")

tbefore, tafter = st.tabs("Початкові дані", "Дані після переведення")

with tbefore:
    renderschool(original)

with tafter:
    #переведення виконується на копії, для порівняння
    promoted = copy.deecopy(original)
    graduated = promoted.promoteall()
    renderschool(promoted)

    st.subheader("Виконується переведення, будь ласка зачекайте...")
    before, after =  original.getstats(), promoted.getstats()
    gradesafter = {c.grade for c in promoted.groups}







