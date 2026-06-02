import streamlit as st

def reguly_card():
    st.page_link("Reguly.py", label=":blue-background[REGUŁY ASOCJACYJNE]")
    #st.markdown("W tej zakładce użytkownik dobiera kategorię oraz miesiąc. Dla wprowadzonych informacji szukane są najlepsze możliwe opcje promocji.")
    st.markdown("Dobierz kategorię detaliczną oraz miesiąc, dla którego chcesz otrzymać sugestie promocji na nią.")

def kategorie_card():
    st.page_link("Kategorie.py", label=":blue-background[KATEGORIE DETALICZNE]")
    #st.markdown("W tej zakładce użytkownik wybiera kategorię. Dla niej program znajduje miesiące, w których istnieją predyspozycje do wprowadzenia promocji cross-selling.")
    st.markdown("Dobierz kategorię detaliczną, aby sprawdzić w jakich miesiącach istnieje potencjał wprowadzenia promocji z wykorzystaniem taktyki cross-selling.")
