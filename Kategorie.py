import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import plotly.express as px
#wczytanie tabelek

st.header(":blue[Kategorie detaliczne]", divider="blue")

P1 = pd.read_csv('dane_streamlit_1.csv', sep=',',decimal=".", index_col=0)
P2 = pd.read_csv('dane_streamlit_2.csv', sep=',',decimal=".", index_col=0)
P3 = pd.read_csv('dane_streamlit_3.csv', sep=',',decimal=".", index_col=0)
P4 = pd.read_csv('dane_streamlit_4.csv', sep=',',decimal=".", index_col=0)
P5 = pd.read_csv('dane_streamlit_5.csv', sep=',',decimal=".", index_col=0)
P6 = pd.read_csv('dane_streamlit_6.csv', sep=',',decimal=".", index_col=0)
Pozycja = pd.concat([P1, P2, P3, P4, P5, P6])

#SŁOWNIKI
file = open('Oferta_slownik.txt')
oferta_slownik = file.read()
file.close()
oferta_slownik = eval(oferta_slownik)

file = open('param_min_s_kat.txt')
param_min_s_kat = file.read()
file.close()
param_min_s_kat = eval(param_min_s_kat)

file = open('param_min_t_kat.txt')
param_min_t_kat = file.read()
file.close()
param_min_t_kat = eval(param_min_t_kat)

miesiac_slownik = {1: "Styczeń", 2: "Luty", 3: "Marzec", 4: "Kwiecień",
    5: "Maj", 6: "Czerwiec", 7: "Lipiec", 8: "Sierpień",
    9: "Wrzesień", 10: "Październik", 11: "Listopad", 12: "Grudzień"}

#NAGLOWEK
col1, = st.columns(1)
kat = col1.selectbox('**Kategoria**:', Pozycja['Kat. detal.'].unique(), index=None)
if not kat:
    kat = 'SRODKI PRZECIWBOLOWE'


m_s = param_min_s_kat[kat]
m_t = param_min_t_kat[kat]



#KOD

ile=0
ktore=[]

Pozycja_kategoria = Pozycja[Pozycja['Kat. detal.'].isin([kat])]
Pozycja_kategoria = Pozycja_kategoria[Pozycja_kategoria['Dostawca NEUCA']==True]
produkty_w_zasadach = set()
for mies in range(1, 13):
    Pozycja_kategoria_m = Pozycja_kategoria[Pozycja_kategoria['Miesiac']==mies]
    Koszyk = pd.crosstab(Pozycja_kategoria_m['Kod dokumentu'],Pozycja_kategoria_m['Kod SAP produktu'])
    Koszyk = Koszyk>0
    zbiory_czeste = apriori(Koszyk, use_colnames = True,min_support = m_s)
    if len(zbiory_czeste)>0:    
        rules = association_rules(zbiory_czeste,metric = 'lift',min_threshold = m_t)
        lenr = len(rules)
        ktore.append(lenr)
        if lenr>0:
            ile += 1
            for _, row in rules.iterrows():
                produkty_w_zasadach.update(row['antecedents'])
                produkty_w_zasadach.update(row['consequents'])


st.write('Reguły asocjacyjne dla kategorii ',kat,' w skali roku')

do_wykresu = pd.DataFrame()
do_wykresu['Liczba reguł'] = ktore
do_wykresu['Miesiąc'] = range(1,13)
do_wykresu['Miesiąc'] = do_wykresu['Miesiąc'].map(miesiac_slownik)
fig = px.line(do_wykresu, y='Liczba reguł', x='Miesiąc')
fig.update_layout(xaxis=dict(type='category'))
st.plotly_chart(fig, theme="streamlit")

wybrane = do_wykresu['Miesiąc'][do_wykresu['Liczba reguł']>0]

st.write(f"**Liczba miesięcy, w których znaleziono reguły asocjacyjne**: {ile}")
st.write(f"**Miesiące z regułami asocjacyjnymi**: {', '.join(wybrane)}.")
st.write(f"**Liczba produktów, które pojawiają się w regułach na przestrzeni całego roku**: {len(produkty_w_zasadach)}")
st.write("\n")
st.write("Lista produktów (nazwy produktów):")
for i in produkty_w_zasadach:
    st.write('*', oferta_slownik[i], '\n')
