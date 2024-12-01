import streamlit as st
from sections import auteur, partenaires, contact, historique, mission, objectifs, vision, perspective, databank, actualites, traitement_donnees

def app():
    # Initialiser la page active si elle n'est pas définie
    if "selected_section" not in st.session_state:
        st.session_state["selected_section"] = "Accueil"

    # Configuration CSS pour l'en-tête et la barre de navigation
    st.markdown("""
    <style>
        /* En-tête */
        .main-header {
            text-align: center;
            padding: 20px;
            background-color: #004080;
            color: white;
            border-bottom: 4px solid #f8f9fa;
        }
        .main-header h2 {
            margin: 0;
            font-size: 36px;
            font-family: 'Arial', sans-serif;
        }

        /* Barre de boutons */
        .button-bar {
            display: flex;
            justify-content: center;
            background-color: #f8f9fa;
            padding: 10px;
            gap: 15px;
            margin-bottom: -20px; /* Réduire davantage l'espace en dessous des boutons */
        }
        .stButton>button {
            background-color: white;
            color: #004080;
            font-size: 16px;
            font-weight: bold;
            padding: 10px 20px;
            border: 2px solid #004080;
            border-radius: 5px;
            min-width: 120px;
            max-width: 180px;
            white-space: nowrap;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #004080;
            color: white;
        }

        /* Conteneur du message principal avec largeur étendue */
        .main-content {
            text-align: center;
            padding: 30px;
            background-color: #f4f4f9;
            border-radius: 5px;
            width: 100%;
            margin-top: -30px; /* Augmenter la marge négative pour réduire davantage l'espace */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # En-tête de l'application
    st.markdown("""
    <div class='main-header'>
        <h2>République Démocratique du Congo</h2>
    </div>
    """, unsafe_allow_html=True)

    # Barre de boutons pour navigation
    st.markdown("<div class='button-bar'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("À PROPOS"):
            st.session_state["selected_section"] = "À PROPOS"
    with col2:
        if st.button("MISSION"):
            st.session_state["selected_section"] = "MISSION"
    with col3:
        if st.button("PERSPECTIVE"):
            st.session_state["selected_section"] = "PERSPECTIVE"
    with col4:
        if st.button("DOCUMENTATION"):
            st.session_state["selected_section"] = "DOCUMENTATION"
    with col5:
        if st.button("CONTACT"):
            st.session_state["selected_section"] = "CONTACT"
    st.markdown("</div>", unsafe_allow_html=True)

    # Message principal sur la page d'accueil avec largeur étendue
    st.markdown("""
    <div class="main-content">
        <h1 style="font-size: 28px; font-family: 'Arial', sans-serif; color: #333;">
            SYSTÈME D'AIDE À LA DÉCISION POUR LA GESTION DES DÉPENSES PUBLIQUES
        </h1>
        <p style="font-size: 18px; color: #666;">Bienvenue dans l'application.</p>
        <p style="font-size: 16px; color: #666;">Choisissez une option dans le menu pour commencer.</p>
    </div>
    """, unsafe_allow_html=True)

    # Affichage du contenu en fonction de la section sélectionnée
    section = st.session_state["selected_section"]

    if section == "À PROPOS":
        st.write("### À PROPOS")
        auteur.app()
        partenaires.app()
        contact.app()

    elif section == "MISSION":
        st.write("### MISSION")
        historique.app()
        mission.app()
        objectifs.app()
        vision.app()
        perspective.app()

    elif section == "PERSPECTIVE":
        st.write("### PERSPECTIVE")
        perspective.app()

    elif section == "DOCUMENTATION":
        st.write("### DOCUMENTATION")
        traitement_donnees.app()
        databank.app()
        actualites.app()

    elif section == "CONTACT":
        st.write("### CONTACT")
        contact.app()