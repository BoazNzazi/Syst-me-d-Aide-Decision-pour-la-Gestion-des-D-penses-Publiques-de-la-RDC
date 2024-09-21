import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def app(df):
    st.header('Visualisation des Données')
    
    # Filtrer les données par année et ministères
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))
    
    ministries = st.multiselect('Sélectionnez les ministères', options=df['Institutions/Ministères'].unique())
    
    filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
    
    if ministries:
        filtered_df = filtered_df[filtered_df['Institutions/Ministères'].isin(ministries)]
    
    st.write(filtered_df)
    
    # Afficher le graphique
    if not filtered_df.empty:
        st.subheader('Graphique des Dépenses par Ministère')
        plt.figure(figsize=(10, 6))
        sns.barplot(data=filtered_df, x='Année', y='Budget Dépense Courante', hue='Institutions/Ministères')
        plt.xticks(rotation=45)
        plt.title('Dépenses par Ministère')
        st.pyplot(plt)
    else:
        st.write("Aucune donnée à afficher pour la sélection actuelle.")

