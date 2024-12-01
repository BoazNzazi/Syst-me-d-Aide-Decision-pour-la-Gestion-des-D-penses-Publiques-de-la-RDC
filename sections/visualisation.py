import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io
import numpy as np

def app(df):
    # Ajouter un style CSS pour l'en-tête et les onglets
    st.markdown("""
    <style>
        /* Style principal de l'en-tête */
        .main-header {
            text-align: center;
            padding: 20px;
            background-color: #004080; /* Couleur bleu foncé */
            color: white;
            border-bottom: 4px solid #f8f9fa;
        }
        .main-header h2 {
            margin: 0;
            font-size: 36px;
            font-family: 'Arial', sans-serif;
        }
        .sub-header {
            text-align: center;
            padding: 10px;
            background-color: #f8f9fa; /* Couleur grise */
            color: #004080;
            font-size: 18px;
            font-weight: bold;
            border-bottom: 4px solid #ddd;
            font-family: 'Arial', sans-serif;
        }

        /* Style des onglets */
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: center; /* Centre les onglets */
            background-color: #f1f1f1; /* Fond gris clair */
            border-bottom: 2px solid #ddd;
        }
        .stTabs [role="tab"] {
            padding: 10px 20px;
            margin: 0 10px;
            font-size: 16px;
            color: #0056b3; /* Texte bleu */
            background-color: transparent;
            border: none;
            font-weight: bold;
        }
        .stTabs [role="tab"]:hover {
            color: #003f7f; /* Couleur plus sombre au survol */
        }
        .stTabs [role="tab"][aria-selected="true"] {
            color: #ffffff; /* Texte blanc */
            background-color: #0056b3; /* Fond bleu pour onglet actif */
            border-radius: 4px; /* Coins arrondis */
        }
    </style>
    """, unsafe_allow_html=True)

    # En-tête de l'application
    st.markdown("""
    <div class='main-header'>
        <h2>République Démocratique du Congo</h2>
    </div>
    <div class='sub-header'>
        SYSTÈME D'AIDE À LA DÉCISION POUR LA GESTION DES DÉPENSES PUBLIQUES
    </div>
    """, unsafe_allow_html=True)

    st.header('Visualisation des Données')

    # Filtrer les données par année
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))

    # Sélection du type de dépenses
    expense_type = st.selectbox("Sélectionnez un type de dépense", 
                                ["Aucun", "Budget Dépense Courante", "Exécution Dépense"])

    # Sélection des ministères
    ministries = st.multiselect('Sélectionnez les ministères (ou laissez vide pour tous)', options=df['Institutions/Ministères'].unique()) if expense_type != "Aucun" else []

    # Filtrer les données selon la sélection
    filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])].copy()
    if ministries:
        filtered_df = filtered_df[filtered_df['Institutions/Ministères'].isin(ministries)]

    filtered_df.replace([np.inf, -np.inf], 0, inplace=True)
    filtered_df.fillna(0, inplace=True)

    # Sélection des indicateurs
    indicators_columns = df.columns[-10:]  # Dernières colonnes comme indicateurs
    selected_indicators = st.multiselect('Sélectionnez les indicateurs à afficher (ou laissez vide pour tous)', options=indicators_columns)

    # Onglets pour les graphiques
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Bar Plot", "Line Plot", "Barres Horizontales", "Pie Chart", "Histogramme", "Barres Empilées"]
    )

    def plot_and_download(fig, title, filename):
        """Affiche le graphique et ajoute un bouton pour télécharger l'image."""
        st.pyplot(fig)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        st.download_button(label=f"Télécharger {title}", data=buf.getvalue(), file_name=filename, mime="image/png")
        buf.seek(0)
        plt.close(fig)

    # Onglet Bar Plot
    with tab1:
        st.subheader(f'Bar Plot : {expense_type if expense_type != "Aucun" else "Indicateurs"}')
        if not filtered_df.empty and expense_type != "Aucun":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', palette="Set1", ax=ax)
            ax.set_title(f'{expense_type} par Année et Ministère')
            ax.tick_params(axis='x', rotation=45)
            ax.legend(loc='upper left')
            plot_and_download(fig, "Bar Plot", f"{expense_type}_bar_plot.png")
        elif not filtered_df.empty and selected_indicators:
            for indicator in selected_indicators:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=filtered_df, x='Année', y=indicator, ax=ax)
                ax.set_title(f'{indicator} par Année')
                ax.tick_params(axis='x', rotation=45)
                plot_and_download(fig, f'Bar Plot pour {indicator}', f"{indicator}_bar_plot.png")
        else:
            st.warning("Aucune donnée disponible pour le Bar Plot.")

    # Onglet Line Plot
    with tab2:
        st.subheader(f'Line Plot : Évolution de {expense_type if expense_type != "Aucun" else "Indicateurs"}')
        if not filtered_df.empty and expense_type != "Aucun":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', marker='o', ax=ax)
            ax.set_title(f"Évolution de {expense_type}")
            ax.tick_params(axis='x', rotation=45)
            ax.legend(loc='upper left')
            plot_and_download(fig, "Line Plot", f"line_plot_{expense_type}.png")
        elif not filtered_df.empty and selected_indicators:
            fig, ax = plt.subplots(figsize=(10, 6))
            for indicator in selected_indicators:
                sns.lineplot(data=filtered_df, x='Année', y=indicator, label=indicator, marker='o', ax=ax)
            ax.set_title("Évolution des indicateurs")
            ax.tick_params(axis='x', rotation=45)
            ax.legend(loc='upper left')
            plot_and_download(fig, "Line Plot", "line_plot_indicators.png")
        else:
            st.warning("Aucune donnée disponible pour le Line Plot.")

    # Onglet Barres Horizontales
    with tab3:
        st.subheader(f'Barres Horizontales : Comparaison des {expense_type if expense_type != "Aucun" else "Indicateurs"}')
        selected_year = st.selectbox('Sélectionnez une année pour comparer', options=sorted(filtered_df['Année'].unique()))
        year_filtered_df = filtered_df[filtered_df['Année'] == selected_year]
        if not year_filtered_df.empty and expense_type != "Aucun":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=expense_type, palette="Set1", ax=ax)
            ax.set_title(f"Comparaison des {expense_type} en {selected_year}")
            plot_and_download(fig, "Barres Horizontales", f"horizontal_bars_{selected_year}.png")
        elif not year_filtered_df.empty and selected_indicators:
            for indicator in selected_indicators:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=indicator, palette="Set1", ax=ax)
                ax.set_title(f"Comparaison de {indicator} en {selected_year}")
                plot_and_download(fig, "Barres Horizontales", f"horizontal_bars_{selected_year}_{indicator}.png")
        else:
            st.warning("Aucune donnée disponible pour les barres horizontales.")

    # Onglet Pie Chart
    with tab4:
        st.subheader(f'Pie Chart : Répartition des {expense_type if expense_type != "Aucun" else "Indicateurs"} en {selected_year}')
        if not year_filtered_df.empty and expense_type != "Aucun":
            pie_data = year_filtered_df.groupby('Institutions/Ministères')[expense_type].sum()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Répartition des {expense_type} par Ministère en {selected_year}")
            plot_and_download(fig, "Pie Chart", f"pie_chart_{selected_year}.png")
        elif not year_filtered_df.empty and selected_indicators:
            for indicator in selected_indicators:
                pie_data = year_filtered_df.groupby('Institutions/Ministères')[indicator].sum()
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Répartition de {indicator} par Ministère en {selected_year}")
                plot_and_download(fig, f"Pie Chart pour {indicator}", f"pie_chart_{selected_year}_{indicator}.png")
        else:
            st.warning("Aucune donnée disponible pour le graphique circulaire.")

    # Onglet Histogramme
    with tab5:
        st.subheader(f'Histogramme : Répartition des {expense_type if expense_type != "Aucun" else "Indicateurs"}')
        if not filtered_df.empty and expense_type != "Aucun":
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=filtered_df, x=expense_type, bins=10, kde=True, ax=ax)
            ax.set_title(f"Histogramme des {expense_type}")
            plot_and_download(fig, "Histogramme", f"histogram_{expense_type}.png")
        elif not filtered_df.empty and selected_indicators:
            for indicator in selected_indicators:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.histplot(data=filtered_df, x=indicator, bins=10, kde=True, ax=ax)
                ax.set_title(f"Histogramme de {indicator}")
                plot_and_download(fig, f"Histogramme pour {indicator}", f"histogram_{indicator}.png")
        else:
            st.warning("Aucune donnée disponible pour l'histogramme.")

    # Onglet Barres Empilées
    with tab6:
        st.subheader(f'Barres Empilées : Répartition des {expense_type if expense_type != "Aucun" else "Indicateurs"}')
        if not filtered_df.empty and expense_type != "Aucun":
            stacked_df = filtered_df.pivot_table(values=expense_type, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
            fig, ax = plt.subplots(figsize=(10, 6))
            stacked_df.plot(kind='bar', stacked=True, colormap='tab20', ax=ax)
            ax.set_title(f"Répartition des {expense_type} par Année")
            plot_and_download(fig, "Barres Empilées", f"stacked_bar_{expense_type}.png")
        elif not filtered_df.empty and selected_indicators:
            for indicator in selected_indicators:
                stacked_df = filtered_df.pivot_table(values=indicator, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
                fig, ax = plt.subplots(figsize=(10, 6))
                stacked_df.plot(kind='bar', stacked=True, colormap='tab20', ax=ax)
                ax.set_title(f"Répartition de {indicator} par Année")
                plot_and_download(fig, f"Barres Empilées pour {indicator}", f"stacked_bar_{indicator}.png")
        else:
            st.warning("Aucune donnée disponible pour les barres empilées.")