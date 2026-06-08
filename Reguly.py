import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


st.header(":blue[Reguły asocjacyjne]", divider="blue")

#WCZYTANIE TABELEK
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

# NAGLOWEK
#st.write('Reguły asocjacyjne dla produktów z wybranej kategorii w wybranym miesiącu')
col1, col2 = st.columns(2)

kat = col1.selectbox('**Kategoria**:', Pozycja['Kat. detal.'].unique(), index=None)
if not kat:
    kat = 'SRODKI PRZECIWBOLOWE'

mies = col2.number_input('Miesiac:', min_value=1, max_value=12, value=6)


#KOD

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
rules_tabelka = rules[['antecedents','consequents','confidence', 'lift']]
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
tabelka_rules['Miara ufności'] = rules_tabelka['confidence']
tabelka_rules['Miara wzrostu'] = rules_tabelka['lift']
tabelka_rules = tabelka_rules.sort_values(['Miara wzrostu', 'Miara ufności'], ascending=False)
tabelka_rules.index = [''] * len(tabelka_rules)


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

prod_neuca = prod[prod['Dostawca NEUCA']==True].groupby(['Kod SAP produktu', 'Znacznik promocja'])['Łączna wartość (pln)'].sum().reset_index()
prod_neuca['Nazwa produktu'] = prod_neuca['Kod SAP produktu'].map(oferta_slownik)
prod_neuca['Znacznik promocja'] = prod_neuca['Znacznik promocja'].map({True:'Prawda', False:'Fałsz'})


prod_nieneuca = prod[prod['Dostawca NEUCA']==False].groupby(['Kod SAP produktu', 'Znacznik promocja'])['Łączna wartość (pln)'].sum().reset_index()
prod_nieneuca['Nazwa produktu'] = prod_nieneuca['Kod SAP produktu'].map(oferta_slownik)
prod_nieneuca['Znacznik promocja'] = prod_nieneuca['Znacznik promocja'].map({True:'Prawda', False:'Fałsz'})

prod_ogolnie = prod.groupby(['Kod SAP produktu', 'Dostawca NEUCA'])['Łączna wartość (pln)'].sum().reset_index()
prod_ogolnie['Dostawca'] = prod_ogolnie['Dostawca NEUCA'].map({True:'Neuca', False:'inni dostawcy'})
prod_ogolnie['Nazwa produktu'] = prod_ogolnie['Kod SAP produktu'].map(oferta_slownik)

st.write('\n')
st.subheader(':blue[Analiza sprzedaży wyróżnionych produktów]')
tab1, tab2= st.tabs(["Udział Neuca w sprzedaży","Występowanie promocji w sprzedaży"])

kolory_dostawca = {"Neuca": "#62c4f0", "inni dostawcy": "#f5b840"}
kolory_promocja = {"Prawda":"#a2f067", "Fałsz":"#e36464"}

with tab1:
    st.write('\n')
    
    stack = st.segmented_control(
        "Wartość na wykresach",
        ["nominalna", "procentowa"],
        key="bar_chart_stack1",)

    st.write('\n')

    if stack=="procentowa":
        prod_ogolnie['Wartość procentowa'] = 100 * prod_ogolnie['Łączna wartość (pln)']/prod_ogolnie.groupby('Kod SAP produktu')['Łączna wartość (pln)'].transform('sum')
        st.write('<u>Sprzedaż wyróżnionych produktów w podziale na dostawcę</u>', unsafe_allow_html=True)
        fig = px.bar(prod_ogolnie, x='Nazwa produktu', y='Wartość procentowa', color='Dostawca', color_discrete_map=kolory_dostawca)
        st.plotly_chart(fig, theme="streamlit")
    else:
        st.write('<u>Sprzedaż wyróżnionych produktów w podziale na dostawcę</u>', unsafe_allow_html=True)
        fig = px.bar(prod_ogolnie, x='Nazwa produktu', y='Łączna wartość (pln)', color='Dostawca', color_discrete_map=kolory_dostawca)
        st.plotly_chart(fig, theme="streamlit")
        
        
    
    

with tab2:
    st.write('\n')
    
    stack = st.segmented_control(
        "Wartość na wykresach",
        ["nominalna", "procentowa"],
        key="bar_chart_stack2",)
    
    st.write('\n')
    
    if stack=="procentowa":
        prod_neuca['Wartość procentowa'] = 100 * prod_neuca['Łączna wartość (pln)']/prod_neuca.groupby('Kod SAP produktu')['Łączna wartość (pln)'].transform('sum')
        prod_nieneuca['Wartość procentowa'] = 100 * prod_nieneuca['Łączna wartość (pln)']/prod_nieneuca.groupby('Kod SAP produktu')['Łączna wartość (pln)'].transform('sum')
        
        st.write('<u>Sprzedaż wyróżnionych produktów przez NEUCA</u>', unsafe_allow_html=True)
        fig = px.bar(prod_neuca, x='Nazwa produktu', y='Wartość procentowa', color='Znacznik promocja', color_discrete_map=kolory_promocja)
        st.plotly_chart(fig, theme="streamlit")
        st.write('\n')
        st.write('\n')
        st.write('<u>Sprzedaż wyróżnionych produktów przez konkurencję</u>', unsafe_allow_html=True)
        fig = px.bar(prod_nieneuca, x='Nazwa produktu', y='Wartość procentowa', color='Znacznik promocja', color_discrete_map=kolory_promocja)
        st.plotly_chart(fig, theme="streamlit")
    
        
    else:
        st.write('<u>Sprzedaż wyróżnionych produktów przez NEUCA</u>', unsafe_allow_html=True)
        fig = px.bar(prod_neuca, x='Nazwa produktu', y='Łączna wartość (pln)', color='Znacznik promocja', color_discrete_map=kolory_promocja)
        st.plotly_chart(fig, theme="streamlit")
        st.write('\n')
        st.write('\n')
        st.write('<u>Sprzedaż wyróżnionych produktów przez konkurencję</u>', unsafe_allow_html=True)
        fig = px.bar(prod_nieneuca, x='Nazwa produktu', y='Łączna wartość (pln)', color='Znacznik promocja', color_discrete_map=kolory_promocja)
        st.plotly_chart(fig, theme="streamlit")
    
