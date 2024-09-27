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
    if expense_type == "Aucun":
        st.warning("Veuillez choisir un type de dépense avant de sélectionner les ministères.")
        ministries = []
    else:
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

    # Remplacer les NaN par 0 pour éviter les erreurs
    filtered_df = filtered_df.replace({np.nan: 0})

    # --- Utilisation d'onglets pour organiser les graphiques ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Bar Plot", "Line Plot", "Barres Horizontales", "Pie Chart", "Histogramme", "Barres Empilées"]
    )

    # ---- Onglet Bar Plot ----
    with tab1:
        st.subheader(f'Graphique des {expense_type if expense_type != "Aucun" else "indicateurs"} par Année (Bar Plot)')
        
        # Graphique pour les dépenses
        if expense_type != "Aucun" and not filtered_df.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères')
            plt.xticks(rotation=45)
            plt.title(f'{expense_type} par Ministère')
            st.pyplot(plt)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"{expense_type}_bar_plot.png", mime="image/png")
            buf.seek(0)
        # Graphique pour plusieurs indicateurs avec comparaison groupée
        elif selected_indicators and not filtered_df.empty:
            plt.figure(figsize=(10, 6))
            bar_width = 0.2  # Ajustement de la largeur des barres pour chaque indicateur

            x = np.arange(len(filtered_df['Année'].unique()))  # Position des barres sur l'axe x

            # Pour chaque indicateur, ajouter des barres décalées
            for i, indicator in enumerate(selected_indicators):
                offset = i * bar_width  # Décalage pour chaque indicateur
                plt.bar(x + offset, filtered_df.groupby('Année')[indicator].mean(), 
                        width=bar_width, label=indicator)

            plt.xticks(x + bar_width * (len(selected_indicators) / 2), filtered_df['Année'].unique(), rotation=45)
            plt.title(f"Comparaison des indicateurs par Année")
            plt.legend(loc='upper right')
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"indicateurs_bar_plot.png", mime="image/png")
            buf.seek(0)
        else:
            st.write("Aucune donnée à afficher pour les dépenses ou les indicateurs.")

    # ---- Onglet Line Plot ----
    with tab2:
        st.subheader(f"Graphique en ligne : Évolution des {expense_type if expense_type != 'Aucun' else 'indicateurs'} dans le Temps")
        
        # Graphique pour les dépenses
        if expense_type != "Aucun" and not filtered_df.empty:
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', marker='o')
            plt.xticks(rotation=45)
            plt.title(f"Évolution des {expense_type} par Ministère")
            plt.ylabel(expense_type)
            plt.xlabel("Année")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"evolution_{expense_type}.png", mime="image/png")
            buf.seek(0)
        # Graphique pour plusieurs indicateurs sur un même graphique
        elif selected_indicators and not filtered_df.empty:
            plt.figure(figsize=(10, 6))
            for indicator in selected_indicators:
                sns.lineplot(data=filtered_df, x='Année', y=indicator, label=indicator, marker='o')
            plt.xticks(rotation=45)
            plt.title(f"Évolution des indicateurs par Année")
            plt.legend(loc='upper right')
            st.pyplot(plt)
            
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

        year_filtered_df = df[(df['Année'] == selected_year) & df['Institutions/Ministères'].isin(ministries)]

        # Graphique pour les dépenses
        if expense_type != "Aucun" and not year_filtered_df.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=expense_type, palette="Set1", dodge=False)
            plt.title(f"Comparaison des {expense_type} entre Ministères en {selected_year}")
            plt.xlabel(expense_type)
            plt.ylabel("Ministères")
            st.pyplot(plt)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"comparaison_{expense_type}_{selected_year}.png", mime="image/png")
            buf.seek(0)
        # Graphique pour les indicateurs
        elif selected_indicators and not year_filtered_df.empty:
            plt.figure(figsize=(10, 6))
            for indicator in selected_indicators:
                sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=indicator, palette="Set1", dodge=False)
            plt.title(f"Comparaison des indicateurs entre Ministères en {selected_year}")
            st.pyplot(plt)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"comparaison_indicateurs_{selected_year}.png", mime="image/png")
            buf.seek(0)
        else:
            st.write(f"Aucune donnée disponible pour l'année sélectionnée ou les ministères.")

    # ---- Onglet Pie Chart ----
    with tab4:
        st.subheader(f"Graphique circulaire : Répartition des {expense_type if expense_type != 'Aucun' else 'indicateurs'} pour l'année {selected_year}")
        
        # Graphique pour les dépenses
        if expense_type != "Aucun" and not year_filtered_df.empty:
            pie_data = year_filtered_df.groupby('Institutions/Ministères')[expense_type].sum()
            if not pie_data.empty and pie_data.sum() > 0:
                plt.figure(figsize=(8, 8))
                plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
                plt.title(f"Répartition des {expense_type} par Ministère en {selected_year}")
                plt.axis('equal')
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label="Télécharger l'image", data=buf, file_name=f"pie_chart_{expense_type}_{selected_year}.png", mime="image/png")
                buf.seek(0)
            else:
                st.write(f"Aucune donnée disponible pour générer le graphique circulaire.")
        # Graphique pour les indicateurs
        elif selected_indicators and not year_filtered_df.empty:
            for indicator in selected_indicators:
                pie_data = year_filtered_df.groupby('Institutions/Ministères')[indicator].sum()
                if not pie_data.empty and pie_data.sum() > 0:
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
        
        # Graphique pour les dépenses
        if expense_type != "Aucun" and not filtered_df.empty:
            plt.figure(figsize=(10, 6))
            sns.histplot(data=filtered_df, x=expense_type, bins=10, kde=False)
            plt.title(f"Répartition des {expense_type} par tranches")
            st.pyplot(plt)

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            st.download_button(label="Télécharger l'image", data=buf, file_name=f"histogramme_{expense_type}.png", mime="image/png")
            buf.seek(0)
        # Graphique pour les indicateurs
        elif selected_indicators and not filtered_df.empty:
            for indicator in selected_indicators:
                plt.figure(figsize=(10, 6))
                sns.histplot(data=filtered_df, x=indicator, bins=10, kde=False)
                plt.title(f"Répartition de l'indicateur {indicator} par tranches")
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label=f"Télécharger l'image pour {indicator}", data=buf, file_name=f"histogramme_{indicator}.png", mime="image/png")
                buf.seek(0)
        else:
            st.write(f"Aucune donnée à afficher pour le graphique en histogramme.")

    # ---- Onglet Barres Empilées ----
    with tab6:
        st.subheader(f"Graphique à barres empilées : Répartition des {expense_type if expense_type != 'Aucun' else 'indicateurs'} par Ministère dans le temps")
        
        # Graphique pour les dépenses
        if expense_type != "Aucun" and not filtered_df.empty:
            stacked_df = filtered_df.pivot_table(values=expense_type, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
            if not stacked_df.empty:
                stacked_df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
                plt.title(f"Répartition des {expense_type} entre Ministères dans le temps")
                plt.ylabel(expense_type)
                st.pyplot(plt)

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                st.download_button(label="Télécharger l'image", data=buf, file_name=f"stacked_bar_{expense_type}.png", mime="image/png")
                buf.seek(0)
        # Graphique pour les indicateurs
        elif selected_indicators and not filtered_df.empty:
            for indicator in selected_indicators:
                stacked_df = filtered_df.pivot_table(values=indicator, index='Année', columns='Institutions/Ministères', aggfunc='sum', fill_value=0)
                if not stacked_df.empty:
                    stacked_df.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
                    plt.title(f"Répartition de l'indicateur {indicator} entre Ministères dans le temps")
                    plt.ylabel(indicator)
                    st.pyplot(plt)

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    st.download_button(label=f"Télécharger l'image pour {indicator}", data=buf, file_name=f"stacked_bar_{indicator}.png", mime="image/png")
                    buf.seek(0)
        else:
            st.write(f"Aucune donnée disponible pour le graphique empilé.")
