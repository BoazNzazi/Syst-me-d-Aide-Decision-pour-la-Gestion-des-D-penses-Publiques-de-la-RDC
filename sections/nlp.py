import streamlit as st
import openai
import pandas as pd
import matplotlib.pyplot as plt
from sections.config import API_KEY  # Importer la clé API

# Configurer la clé API d'OpenAI
openai.api_key = API_KEY

# Fonction pour interroger GPT-3.5 et analyser la question
def query_gpt3_5(question):
    try:
        # Appel à GPT-3.5 pour interpréter la question
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=150
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erreur : {str(e)}"

# Fonction pour interroger le DataFrame en fonction des résultats de GPT-3.5
def query_dataframe(df, query):
    if "espérance de vie" in query.lower():
        result = df[['Année', 'Espérance de Vie']]
        return result
    elif "PIB" in query.lower():
        result = df[['Année', 'PIB/Hab']]
        return result
    elif "chômage" in query.lower():
        result = df[['Année', 'Taux Chomage']]
        return result
    else:
        return "Désolé, je n'ai pas trouvé d'information pertinente pour votre question."

# Fonction principale pour l'interrogation NLP
def app(df):
    # En-tête avec "République Démocratique du Congo"
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #007bff; color: white;'>
        <h2 style='margin: 0;'>République Démocratique du Congo</h2>
    </div>
    """, unsafe_allow_html=True)

    # Nouvelle barre de navigation avec le titre
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
    </style>
    <div class="nav-links">
        <a href="#analyse-avancee" target="_self">SYSTÈME D'AIDE À LA DÉCISION POUR LA GESTION DES DÉPENSES PUBLIQUES</a>
    </div>
    """, unsafe_allow_html=True)

    st.header('Interrogation en Langage Naturel')

    # Zone de texte pour poser une question en langage naturel
    question = st.text_input('Posez une question ou entrez une commande :')

    if question:
        # Appel à GPT-3.5 pour obtenir une analyse de la question
        response = query_gpt3_5(question)
        st.write('Interprétation de GPT-3.5 : ', response)

        # Interroger le jeu de données en fonction de l'interprétation
        result = query_dataframe(df, response)
        
        # Afficher les résultats sous forme de tableau
        if isinstance(result, pd.DataFrame):
            st.write(result)
        else:
            st.write(result)

        # Option pour générer un graphique basé sur les résultats (si applicable)
        if isinstance(result, pd.DataFrame) and 'Année' in result.columns:
            graph_type = st.selectbox('Choisissez le type de graphique', ['Bar Plot', 'Line Plot'])
            generate_plot(result, 'Année', result.columns[1], graph_type)

# Fonction pour générer différents types de graphiques
def generate_plot(df, x_column, y_column, graph_type):
    plt.figure(figsize=(10, 6))
    
    if graph_type == "Bar Plot":
        df.plot(kind='bar', x=x_column, y=y_column)
        plt.title(f'{graph_type} de {y_column} par {x_column}')
    elif graph_type == "Line Plot":
        plt.plot(df[x_column], df[y_column], marker='o')
        plt.title(f'{graph_type} de {y_column} au fil des {x_column}')
    
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.grid(True)
    st.pyplot(plt)
