import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#wczytanie tabelek
#Apteka = pd.read_csv('Apteka.csv', sep=',',decimal=".")
#Dokumenty = pd.read_csv('Dokumenty_bez_SQ.csv', sep=',',decimal=".")

st.title("Sprzedaż dla kategorii")
#Pozycja = pd.read_csv('dane_streamlit.csv', sep=',',decimal=".")

#Produkty = pd.read_csv('Produkty_bez_urz.csv', sep=',',decimal=".")
P1 = pd.read_csv('dane_streamlit_1.csv', sep=',',decimal=".", index_col=0)
P2 = pd.read_csv('dane_streamlit_2.csv', sep=',',decimal=".", index_col=0)
P3 = pd.read_csv('dane_streamlit_3.csv', sep=',',decimal=".", index_col=0)
P4 = pd.read_csv('dane_streamlit_4.csv', sep=',',decimal=".", index_col=0)
P5 = pd.read_csv('dane_streamlit_5.csv', sep=',',decimal=".", index_col=0)
P6 = pd.read_csv('dane_streamlit_6.csv', sep=',',decimal=".", index_col=0)
Pozycja_nowa = pd.concat([P1, P2, P3, P4, P5, P6])

#slowniki - miesiące i parametry 
miesiac_slownik = {1: "Styczeń", 2: "Luty", 3: "Marzec", 4: "Kwiecień",
    5: "Maj", 6: "Czerwiec", 7: "Lipiec", 8: "Sierpień",
    9: "Wrzesień", 10: "Październik", 11: "Listopad", 12: "Grudzień"}
#0.04
#1.2



param_min_s_kat = {'DIABETOLOGIA':0.15, 'PARAZYTOLOGIA':0.1,'OPATRUNKI I MATERIALY HIGIENICZNE':0.13,
                  'UKLAD POKARMOWY':0.3,'SRODKI PRZECIWBOLOWE':0.22,'UKLAD MOCZOWY':0.08,
                   'KARDIOLOGIA':0.18,'ALERGIA':0.09,'PRZEZIEBIENIE':0.265,'SRODKI WZMACNIAJACE':0.28,
                  'UKLAD NERWOWY':0.16,'UKLAD PLCIOWY':0.085,'DERMATOLOGIA':0.095,
                   
                   'STAWY I KOSCI':0.07,'KOSMETYKI':0.08,'SZCZEPIONKI I SUROWICE':0.04,
                  'STOMATOLOGIA':0.11,'NUTRIKOSMETYKI':0.06,
                   'HORMONY OGOLNOUSTROJOWE (Z WYLACZENIEM HORMONOW PLCIOWYCH)':0.05,
                  'NARZADY ZMYSLOW':0.06,'ZYWNOSC I ZIOLOLECZNICTWO':0.07,
                  'ANTYKONCEPCJA':0.07,'UKLAD ODDECHOWY':0.05,'SPRZET MEDYCZNY':0.04,
                  'PLODNOSC I CIAZA':0.08,'SEZON OWADY':0.03}

param_min_t_kat = {'DIABETOLOGIA':1.8, 'PARAZYTOLOGIA':1.2,'OPATRUNKI I MATERIALY HIGIENICZNE':1.4 ,
                  'UKLAD POKARMOWY':1.5,'SRODKI PRZECIWBOLOWE':2.2,'UKLAD MOCZOWY':2.2,
                  'KARDIOLOGIA':1.5,'ALERGIA':2.2,'PRZEZIEBIENIE':2.5,'SRODKI WZMACNIAJACE':1.6,
                  'UKLAD NERWOWY':2,'UKLAD PLCIOWY':2.4,'DERMATOLOGIA':2.99,
                   
                   'STAWY I KOSCI':2.5,'KOSMETYKI':4,'SZCZEPIONKI I SUROWICE':2,
                  'STOMATOLOGIA':2.5,'NUTRIKOSMETYKI':3,
                  'HORMONY OGOLNOUSTROJOWE (Z WYLACZENIEM HORMONOW PLCIOWYCH)':3.5,
                  'NARZADY ZMYSLOW':5,'ZYWNOSC I ZIOLOLECZNICTWO':2,
                  'ANTYKONCEPCJA':2.5,'UKLAD ODDECHOWY':2,'SPRZET MEDYCZNY':3,
                  'PLODNOSC I CIAZA':2, 'SEZON OWADY':3}


#nagłówek strony
st.write('Reguły asocjacyjne dla podanej kategorii w skali roku')
col1, = st.columns(1)
#kat = col1.text_input('Kategoria:', value='PARAZYTOLOGIA')
kat = col1.selectbox('Kategoria:', Pozycja['Kat. detal.'].unique(), index=None)
if not kat:
    kat = 'PARAZYTOLOGIA'


if kat in param_min_s_kat.keys():
    m_s = param_min_s_kat[kat]
    m_t = param_min_t_kat[kat]
else:
    m_s = 0.08
    m_t=2

#kod

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
        

#st.write(ile, '\n')
do_wykresu = pd.DataFrame()#(colnames=['Liczba regul', 'Miesiace'])
do_wykresu['Liczba reguł'] = ktore
do_wykresu['Miesiace'] = range(1,13)
st.line_chart(data=do_wykresu, y='Liczba reguł', x='Miesiace')

wybrane = do_wykresu[do_wykresu['Liczba reguł']>0]
wybrane = [miesiac_slownik[i] for i in wybrane['Miesiace']]

st.write(f"Liczba miesięcy, w których znaleziono reguły asocjacyjne: {ile}")
st.write(f"Miesiące z regułami asocjacyjnymi: {', '.join(wybrane)}.")
st.write(f"Liczba produktów, które pojawiają się w regułach na przestrzeni całego roku: {len(produkty_w_zasadach)}")
st.write("Lista produktów (kody SAP):")
st.write(produkty_w_zasadach)