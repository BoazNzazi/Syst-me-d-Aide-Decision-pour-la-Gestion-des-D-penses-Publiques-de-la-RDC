import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io
import numpy as np

def app(df):
    st.header('Visualisation des Données')

    # Filtrer les données par année
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))

    # Sélection du type de dépenses
    expense_type = st.selectbox("Sélectionnez un type de dépense (ou laissez vide pour ignorer)", 
                                ["Aucun", "Budget Dépense Courante", "Exécution Dépense"])

    # Sélection des ministères
    ministries = []
    if expense_type != "Aucun":
        ministries = st.multiselect('Sélectionnez les ministères (ou laissez vide pour tous)', 
                                    options=df['Institutions/Ministères'].unique())

    # Filtrer les données selon la sélection
    filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
    if ministries:
        filtered_df = filtered_df[filtered_df['Institutions/Ministères'].isin(ministries)]

    # Sélection des indicateurs
    indicators_columns = df.columns[-10:]  # Dernières colonnes comme indicateurs
    selected_indicators = st.multiselect('Sélectionnez les indicateurs à afficher (ou laissez vide)', 
                                         options=indicators_columns)

    # Remplacer les NaN par 0 pour éviter les erreurs dans les graphiques
    filtered_df = filtered_df.fillna(0)

    # --- Utilisation d'onglets pour organiser les graphiques ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Bar Plot", "Line Plot", "Barres Horizontales", "Pie Chart", "Histogramme", "Barres Empilées"]
    )

    # ---- Onglet Bar Plot ----
    with tab1:
        st.subheader(f'Graphique des {expense_type if expense_type != "Aucun" else "indicateurs"} par Année (Bar Plot)')
        
        if expense_type != "Aucun" and not filtered_df.empty:
            # Graphique pour les ministères
            plt.figure(figsize=(10, 6))
            sns.barplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', palette="Set1")
            plt.xticks(rotation=45)
            plt.title(f'{expense_type} par Ministère')
            plt.legend(loc='upper right')
            st.pyplot(plt)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"{expense_type}_bar_plot.png", mime="image/png")
            buf.seek(0)
        
        elif selected_indicators and not filtered_df.empty:
            # Graphique pour les indicateurs (chaque indicateur a une barre par année)
            plt.figure(figsize=(10, 6))
            bar_width = 0.2  # Largeur des barres pour chaque indicateur

            # Tracer chaque indicateur comme une barre distincte
            for i, indicator in enumerate(selected_indicators):
                plt.bar(
                    filtered_df['Année'] + i * bar_width, 
                    filtered_df[indicator], 
                    width=bar_width, 
                    label=indicator
                )

            # Ajuster les positions de l'axe X
            plt.xticks(filtered_df['Année'] + bar_width * (len(selected_indicators) / 2), filtered_df['Année'].astype(int))
            plt.legend(loc='upper right')
            plt.title(f"Comparaison des indicateurs par Année")
            st.pyplot(plt)

            # Ajouter un bouton pour télécharger le graphique
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"indicateurs_bar_plot.png", mime="image/png")
            buf.seek(0)

        else:
            st.write("Aucune donnée à afficher pour les dépenses ou les indicateurs.")

    # ---- Onglet Line Plot ----
    with tab2:
        st.subheader(f"Graphique en ligne : Évolution des {expense_type if expense_type != 'Aucun' else 'indicateurs'} dans le Temps")
        
        if expense_type != "Aucun" and not filtered_df.empty:
            # Graphique pour les ministères
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', marker='o')
            plt.xticks(rotation=45)
            plt.title(f"Évolution des {expense_type} par Ministère")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"evolution_{expense_type}.png", mime="image/png")
            buf.seek(0)
        
        elif selected_indicators and not filtered_df.empty:
            # Graphique pour plusieurs indicateurs (lignes multiples pour chaque indicateur)
            plt.figure(figsize=(10, 6))
            for indicator in selected_indicators:
                sns.lineplot(data=filtered_df, x='Année', y=indicator, label=indicator, marker='o')
            
            plt.xticks(rotation=45)
            plt.title(f"Évolution des indicateurs par Année")
            plt.legend(loc='upper right')
            st.pyplot(plt)

            # Ajouter un bouton pour télécharger le graphique
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"evolution_indicateurs.png", mime="image/png")
            buf.seek(0)
        else:
            st.write("Aucune donnée à afficher pour les indicateurs.")

    # ---- Onglet Barres Horizontales ----
    with tab3:
        st.subheader(f"Graphique à barres horizontales : Comparaison des ministères ou indicateurs pour une année donnée")
        selected_year = st.selectbox('Sélectionnez une année pour comparer', options=sorted(df['Année'].unique()))

        year_filtered_df = filtered_df[filtered_df['Année'] == selected_year]

        if expense_type != "Aucun" and not year_filtered_df.empty:
            # Graphique pour les ministères
            plt.figure(figsize=(10, 6))
            sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=expense_type, hue='Institutions/Ministères', palette="Set1", dodge=False)
            plt.title(f"Comparaison des {expense_type} entre Ministères en {selected_year}")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"comparaison_{expense_type}_{selected_year}.png", mime="image/png")
            buf.seek(0)

        elif selected_indicators and not year_filtered_df.empty:
            # Graphique pour les indicateurs
            plt.figure(figsize=(10, 6))
            melted_df = year_filtered_df[selected_indicators].melt()
            sns.barplot(data=melted_df, y='variable', x='value', hue='variable', palette="Set2", dodge=False)
            plt.title(f"Comparaison des indicateurs en {selected_year}")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"comparaison_indicateurs_{selected_year}.png", mime="image/png")
            buf.seek(0)
        else:
            st.write(f"Aucune donnée disponible pour l'année {selected_year}.")

    # ---- Onglet Pie Chart ----
    with tab4:
        st.subheader(f"Graphique circulaire : Répartition des {expense_type if expense_type != 'Aucun' else 'indicateurs'} pour l'année {selected_year}")
        
        if expense_type != "Aucun" and not year_filtered_df.empty:
            pie_data = year_filtered_df.groupby('Institutions/Ministères')[expense_type].sum()
            if not pie_data.empty:
                plt.figure(figsize=(8, 8))
                plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                plt.title(f"Répartition des {expense_type} par Ministère en {selected_year}")
                plt.axis('equal')
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label="Télécharger l'image", data=buf, file_name=f"pie_chart_{expense_type}_{selected_year}.png", mime="image/png")
                buf.seek(0)

        elif selected_indicators and not year_filtered_df.empty:
            for indicator in selected_indicators:
                pie_data = year_filtered_df.groupby('Institutions/Ministères')[indicator].sum()
                if not pie_data.empty:
                    plt.figure(figsize=(8, 8))
                    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                    plt.title(f"Répartition de l'indicateur {indicator} par Ministère en {selected_year}")
                    plt.axis('equal')
                    st.pyplot(plt)

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    st.download_button(label=f"Télécharger l'image pour {indicator}", data=buf, file_name=f"pie_chart_{indicator}_{selected_year}.png", mime="image/png")
                    buf.seek(0)
        else:
            st.write(f"Aucune donnée disponible pour l'année {selected_year}.")

    # ---- Onglet Histogramme ----
    with tab5:
        st.subheader(f"Graphique en histogramme : Répartition des {expense_type if expense_type != 'Aucun' else 'indicateurs'} par tranches")
        
        if expense_type != "Aucun" and not filtered_df.empty:
            # Histogramme pour les ministères
            plt.figure(figsize=(10, 6))
            sns.histplot(data=filtered_df, x=expense_type, bins=10)
            plt.title(f"Répartition des {expense_type} par tranches")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"histogramme_{expense_type}.png", mime="image/png")
            buf.seek(0)

        elif selected_indicators and not filtered_df.empty:
            # Histogramme pour les indicateurs
            for indicator in selected_indicators:
                plt.figure(figsize=(10, 6))
                sns.histplot(data=filtered_df, x=indicator, bins=10)
                plt.title(f"Répartition de l'indicateur {indicator} par tranches")
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label=f"Télécharger l'image pour {indicator}", data=buf, file_name=f"histogramme_{indicator}.png", mime="image/png")
                buf.seek(0)
        else:
            st.write(f"Aucune donnée à afficher pour l'histogramme.")

    # ---- Onglet Barres Empilées ----
    with tab6:
        st.subheader(f"Graphique à barres empilées : Répartition des {expense_type if expense_type != 'Aucun' else 'indicateurs'} par Ministère dans le temps")
        
        if expense_type != "Aucun" and not filtered_df.empty:
            # Barres empilées pour les ministères
            stacked_df = filtered_df.pivot_table(values=expense_type, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
            stacked_df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
            plt.title(f"Répartition des {expense_type} entre Ministères dans le temps")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"stacked_bar_{expense_type}.png", mime="image/png")
            buf.seek(0)

        elif selected_indicators and not filtered_df.empty:
            # Barres empilées pour les indicateurs
            for indicator in selected_indicators:
                stacked_df = filtered_df.pivot_table(values=indicator, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
                stacked_df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
                plt.title(f"Répartition de l'indicateur {indicator} entre Ministères dans le temps")
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label=f"Télécharger l'image pour {indicator}", data=buf, file_name=f"stacked_bar_{indicator}.png", mime="image/png")
                buf.seek(0)
        else:
            st.write(f"Aucune donnée disponible pour le graphique empilé.")
