
import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

st.title("Reguły asocjacyjne")

#wczytanie tabelek
#Apteka = pd.read_csv('Apteka.csv', sep=',',decimal=".")
#Dokumenty = pd.read_csv('Dokumenty_bez_SQ.csv', sep=',',decimal=".")

###Pozycja_neuca = pd.read_csv('NEUCA_Pozycja_miesiac_i_kod.csv', sep=',',decimal=".")
###Pozycja_nieneuca = pd.read_csv('NIENEUCA_Pozycja_miesiac_i_kod.csv', sep=',',decimal=".")
#Pozycja = pd.read_csv('dane_streamlit.csv', sep=',',decimal=".")

#Produkty = pd.read_csv('Produkty_bez_urz.csv', sep=',',decimal=".")

P1 = pd.read_csv('dane_streamlit_1.csv', sep=',',decimal=".", index_col=0)
P2 = pd.read_csv('dane_streamlit_2.csv', sep=',',decimal=".", index_col=0)
P3 = pd.read_csv('dane_streamlit_3.csv', sep=',',decimal=".", index_col=0)
P4 = pd.read_csv('dane_streamlit_4.csv', sep=',',decimal=".", index_col=0)
P5 = pd.read_csv('dane_streamlit_5.csv', sep=',',decimal=".", index_col=0)
P6 = pd.read_csv('dane_streamlit_6.csv', sep=',',decimal=".", index_col=0)
Pozycja = pd.concat([P1, P2, P3, P4, P5, P6])

#slownik - oferta
file = open('Oferta_slownik.txt')
oferta_slownik = file.read()
file.close()
oferta_slownik = eval(oferta_slownik)

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
                  'ANTYKONCEPCJA':0.07,'UKLAD ODDECHOWY':0.05,'SPRZET MEDYCZNY':0.08,
                  'PLODNOSC I CIAZA':0.08,'SEZON OWADY':0.03}

param_min_t_kat = {'DIABETOLOGIA':1.8, 'PARAZYTOLOGIA':1.2,'OPATRUNKI I MATERIALY HIGIENICZNE':1.4 ,
                  'UKLAD POKARMOWY':1.5,'SRODKI PRZECIWBOLOWE':2.2,'UKLAD MOCZOWY':2.2,
                  'KARDIOLOGIA':1.5,'ALERGIA':2.2,'PRZEZIEBIENIE':2.5,'SRODKI WZMACNIAJACE':1.6,
                  'UKLAD NERWOWY':2,'UKLAD PLCIOWY':2.4,'DERMATOLOGIA':2.99,
                   
                   'STAWY I KOSCI':2.5,'KOSMETYKI':4,'SZCZEPIONKI I SUROWICE':2,
                  'STOMATOLOGIA':2.5,'NUTRIKOSMETYKI':3,
                  'HORMONY OGOLNOUSTROJOWE (Z WYLACZENIEM HORMONOW PLCIOWYCH)':3.5,
                  'NARZADY ZMYSLOW':5,'ZYWNOSC I ZIOLOLECZNICTWO':2,
                  'ANTYKONCEPCJA':2.5,'UKLAD ODDECHOWY':2,'SPRZET MEDYCZNY':1.7,
                  'PLODNOSC I CIAZA':2, 'SEZON OWADY':3}

#nagłówek strony
st.write('Reguły asocjacyjne dla produktów z wybranej kategorii w wybranym miesiącu')
col1, col2 = st.columns(2)
#kat = col1.text_input('Kategoria:', value='PARAZYTOLOGIA')
kat = col1.selectbox('Kategoria:', Pozycja['Kat. detal.'].unique(), index=None)
if not kat:
    kat = 'SRODKI PRZECIWBOLOWE'
mies = col2.number_input('Miesiac:', min_value=1, max_value=12, value=6)


#kod


m_s = param_min_s_kat[kat]
m_t = param_min_t_kat[kat]

Pozycja_kategoria = Pozycja[Pozycja['Kat. detal.'].isin([kat])]
Pozycja_kategoria = Pozycja_kategoria[Pozycja_kategoria['Miesiac']==mies]
Pozycja_kategoria_neuca = Pozycja_kategoria[Pozycja_kategoria['Dostawca NEUCA']==True]

if len(Pozycja_kategoria_neuca['Kod SAP produktu'].unique().tolist())==0:
    st.write('Nie sprzedano żadnego produktu z kategorii ', kat, ' w miesiącu ', miesiac_slownik[mies])
    st.stop()

Koszyk = pd.crosstab(Pozycja_kategoria_neuca['Kod dokumentu'],Pozycja_kategoria_neuca['Kod SAP produktu'])
Koszyk = Koszyk>0
zbiory_czeste = apriori(Koszyk, use_colnames = True,min_support = m_s)
rules = association_rules(zbiory_czeste,metric = 'lift',min_threshold = m_t)
rules_tabelka = rules[['antecedents','consequents', 'lift']]
tabelka_rules = pd.DataFrame()
poprzednicy = []
for x in rules_tabelka['antecedents']:
    pom = set()
    for i in x:
        pom.add(oferta_slownik[i])
    poprzednicy.append(pom)
nastepnicy = []
for x in rules_tabelka['consequents']:
    pom = set()
    for i in x:
        pom.add(oferta_slownik[i])
    nastepnicy.append(pom)
tabelka_rules['Poprzednicy'] = poprzednicy
tabelka_rules['Nastepnicy'] = nastepnicy
tabelka_rules['Wzrost zakupu'] = rules_tabelka['lift']


#przygotowanie do rysowania wykresu 
p = set()
for i in rules['antecedents']:
    i = list(i)
    for j in i:
        p.add(j)
for i in rules['consequents']:
    i = list(i)
    for j in i:
        p.add(j)   
        
prod = Pozycja_kategoria[Pozycja_kategoria['Kod SAP produktu'].isin(p)]
prod['Znacznik promocja'] = prod['Znacznik promocja'].astype(bool)

#wyświetlanie wyniku kodu
if len(p)>0:
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('Reguły dla kategorii ', kat, ' w miesiącu ', miesiac_slownik[mies])
    #st.table(rules_tabelka.applymap(lambda x: tuple(x) if isinstance(x, frozenset) else x ))
    st.table(tabelka_rules)

else:
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('Dla kategorii ', kat, ' w miesiącu ', miesiac_slownik[mies], ' nie znaleziono istotnych reguł asocjacyjnych. Proponujemy skupić się na promocjach na pojedyncze produkty. Poniżej produkty, które przyniosły w tej kategorii i miesiącu największe zyski: ')
    nowa = pd.DataFrame(columns=['Kod SAP', 'Łączna wartość (pln)'])
    nowa['Kod SAP'] = Pozycja_kategoria_neuca['Kod SAP produktu'].unique().tolist()
    k=0
    for i in Pozycja_kategoria_neuca['Kod SAP produktu'].unique():
        pom = Pozycja_kategoria_neuca[Pozycja_kategoria_neuca['Kod SAP produktu']==i]
        wartosc = sum(pom['Wartosc'])
        nowa.loc[k] = [i, wartosc]
        k+=1
    nowa['Łączna wartość (pln)'] = pd.to_numeric(nowa['Łączna wartość (pln)'], errors='coerce')
    top3 = nowa.nlargest(3, "Łączna wartość (pln)")
    p = set(top3['Kod SAP'])
    top3['Nazwa produktu'] = [oferta_slownik[i] for i in top3['Kod SAP']]
    top3 = top3[['Nazwa produktu','Łączna wartość (pln)']]
    st.table(top3)

prod = Pozycja_kategoria[Pozycja_kategoria['Kod SAP produktu'].isin(p)]
prod['Znacznik promocja'] = prod['Znacznik promocja'].astype(bool)

prod = prod.rename(columns={'Wartosc' : 'Łączna wartość (pln)'})
prod['Znacznik promocja'] = prod['Znacznik promocja'].map({True:'Prawda', False:'Fałsz'})

prod_neuca = prod[prod['Dostawca NEUCA']==True].groupby(['Kod SAP produktu', 'Znacznik promocja'])['Łączna wartość (pln)'].sum().reset_index()
prod_neuca['Nazwa produktu'] = prod_neuca['Kod SAP produktu'].map(oferta_slownik)

prod_nieneuca = prod[prod['Dostawca NEUCA']==False].groupby(['Kod SAP produktu', 'Znacznik promocja'])['Łączna wartość (pln)'].sum().reset_index()
prod_nieneuca['Nazwa produktu'] = prod_nieneuca['Kod SAP produktu'].map(oferta_slownik)

st.write('\n')
st.write('\n')
st.write('Sprzedaż wyróżnionych produktów przez NEUCA')
st.write('\n')
st.bar_chart(data=prod_neuca, x='Nazwa produktu', y='Łączna wartość (pln)', color='Znacznik promocja')


st.write('\n')
st.write('\n')
st.write('Sprzedaż wyróżnionych produktów przez konkurencję')
st.write('\n')
st.bar_chart(data=prod_nieneuca, x='Nazwa produktu', y='Łączna wartość (pln)', color='Znacznik promocja')

    