import streamlit as st
import pandas as pd
from sections import accueil, data, visualisation, analyse, nlp, apropos

# Charger le fichier Excel
df = pd.read_excel('FINAL_WITH_ALL_INDICATEURS.xlsx')

# Menu de navigation principal dans la barre latérale
menu = st.sidebar.selectbox('Menu', ['Accueil', 'Data', 'Visualisation', 'Analyse', 'NLP', 'À Propos'])

# Rediriger vers la page choisie
if menu == 'Accueil':
    accueil.app()
elif menu == 'Data':
    data.app(df)
elif menu == 'Visualisation':
    visualisation.app(df)
elif menu == 'Analyse':
    analyse.app(df)
elif menu == 'NLP':
    nlp.app(df)
elif menu == 'À Propos':
    apropos.app()



