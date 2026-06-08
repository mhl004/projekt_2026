import streamlit as st
from cards import (reguly_card, kategorie_card)

st.title(":blue[Trafione oferty, ]")
st.header("**:blue[czyli promocje na podstawie historii zakupów]**", divider="blue")
st.markdown("\n")
st.markdown("\n")

cols = st.columns(2)
with cols[0].container(height=200):
    kategorie_card()
with cols[1].container(height=200):
    reguly_card()
