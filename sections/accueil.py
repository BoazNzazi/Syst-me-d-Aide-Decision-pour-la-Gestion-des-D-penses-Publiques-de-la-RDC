import streamlit as st

def app():
    # En-tête avec "République Démocratique du Congo"
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #007bff; color: white;'>
        <h2 style='margin: 0;'>République Démocratique du Congo</h2>
    </div>
    """, unsafe_allow_html=True)

    # Barre de navigation avec des liens textuels
    st.markdown("""
    <style>
    .nav-links {
        display: flex;
        justify-content: center;
        background-color: #f8f9fa;
        padding: 10px;
        border-bottom: 2px solid #ddd;
    }
    .nav-links a {
        margin: 0 15px;
        text-decoration: none;
        color: #007bff;
        font-size: 18px;
        font-weight: bold;
    }
    .nav-links a:hover {
        text-decoration: underline;
        color: #0056b3;
    }
    </style>
    <div class="nav-links">
        <a href="#apropos" target="_self">À PROPOS</a>
        <a href="#notre-mission" target="_self">NOTRE MISSION</a>
        <a href="#documentation" target="_self">DOCUMENTATION</a>
    </div>
    """, unsafe_allow_html=True)

    # Contenu de l'accueil
    st.title("SYSTÈME D'AIDE À LA DÉCISION POUR LA GESTION DES DÉPENSES PUBLIQUES")
    st.write("Bienvenue dans l'application.")
    st.write("Choisissez une option dans le menu pour commencer.")

# Exécution de l'application
if __name__ == '__main__':
    app()



















