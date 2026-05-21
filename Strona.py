import streamlit as st

st.markdown("""
<style>
[data-testid="stPageLink"] a {
    border: 2px solid #808080;
    border-radius: 10px;
    padding: 8px 12px;
    background-color: #00FFFFF;
}

[data-testid="stPageLink"] a:hover {
    border-color: #4169E1;
    background-color: #00FFFFF;
}
</style>
""", unsafe_allow_html=True)


st.title("Strona główna")
st.write('\n')
st.write('\n')
st.write('<u>REGUŁY ASOCJACYJNE</u>', unsafe_allow_html=True)
st.write('W tej zakładce użytkownik dobiera kategorię oraz miesiąc. W wyniku działania modelu, strona zwraca pary lub zestawy konkretnych produktów, dla których opłaca się wprowadzać promocje łączone. W przypadku nieznalezienia istotnych zależności, użytkownik uzyskuje informacje na temat innych sugestii działania.')
st.page_link(page='pages/Reguly.py',label = "Reguły")
st.write('\n')
st.write('\n')
st.write('<u>ANALIZA KATEGORII</u>', unsafe_allow_html=True)
st.write('W tej zakładce użytkownik wybiera kategorię. Dla niej program znajduje miesiące, w których istnieją istotne powiązania i predyspozycje do wprowadzenia promocji łączonych.')
st.page_link(page='pages/Kategorie.py',label = "Kategorie")
st.write('\n')
st.write('\n')

