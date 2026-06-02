import streamlit as st
from cards import (reguly_card, kategorie_card)

#st.title("Trafione oferty, czyli promocje na podstawie historii zakupów")

pages = [
    st.Page(
        "Strona.py",
        title="Strona główna"
    ),
    st.Page(
        "Reguly.py",
        title="Reguły asocjacyjne"
    ),
    st.Page(
        "Kategorie.py",
        title="Kategorie"
    )
]

page = st.navigation(pages)
page.run()

with st.sidebar.container(height=250):
    if page.title == "Reguły asocjacyjne":
        reguly_card()
    elif page.title == "Kategorie":
        kategorie_card()
    else:
        st.page_link("Strona.py", label=":blue-background[STRONA GŁÓWNA]")
        st.write("Wybierz podstronę z powyższej listy.")
