import streamlit as st
import pandas as pd
from sections import accueil, data, visualisation, analyse, nlp, apropos

# Assurez-vous que cette ligne est la première commande Streamlit
st.set_page_config(page_title="Application de Gestion", layout="wide")

# Charger le fichier Excel
df = pd.read_excel('FINAL_WITH_ALL_INDICATEURS.xlsx')

# Initialiser la sélection dans `st.session_state`
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = "Accueil"

# Menu de navigation principal dans la barre latérale
menu = st.sidebar.selectbox(
    'Menu', 
    ['Accueil', 'Data', 'Visualisation', 'Analyse', 'NLP', 'À Propos'],
    index=['Accueil', 'Data', 'Visualisation', 'Analyse', 'NLP', 'À Propos'].index(st.session_state["selected_menu"])
)

# Mettre à jour la sélection actuelle dans `st.session_state`
st.session_state["selected_menu"] = menu

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
