import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def app(df):
    st.header('Visualisation des Données')

    # Filtrer les données par année (plage de dates déplacée en haut)
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))

    # Sélection du type de dépenses avec possibilité de ne rien choisir
    expense_type = st.selectbox("Sélectionnez un type de dépense (ou laissez vide pour ignorer)", 
                                ["Aucun", "Budget Dépense Courante", "Exécution Dépense"])

    # Afficher un message si aucun type de dépense n'est sélectionné avant la sélection des ministères
    if expense_type == "Aucun":
        st.warning("Veuillez d'abord choisir un type de dépense avant de sélectionner les ministères.")
        ministries = []
    else:
        # Sélection des ministères après avoir choisi le type de dépense
        ministries = st.multiselect('Sélectionnez les ministères (ou laissez vide pour tous)', 
                                    options=df['Institutions/Ministères'].unique())

    # Filtrer les données après la sélection de la plage d'années et des ministères
    filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
    
    if ministries:
        filtered_df = filtered_df[filtered_df['Institutions/Ministères'].isin(ministries)]
    
    # Sélection des indicateurs avec possibilité de ne rien choisir
    indicators_columns = df.columns[-10:]  # Dernières colonnes comme indicateurs
    selected_indicator = st.selectbox('Sélectionnez un indicateur à afficher (ou laissez vide)', 
                                      options=["Aucun"] + list(indicators_columns))

    # Afficher le graphique à barres (Bar Plot) pour les dépenses si un type de dépense est sélectionné
    if expense_type != "Aucun" and not filtered_df.empty:
        st.subheader(f'Graphique des {expense_type} par Ministère (Bar Plot)')
        plt.figure(figsize=(10, 6))
        sns.barplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères')
        plt.xticks(rotation=45)
        plt.title(f'{expense_type} par Ministère')
        plt.legend(loc='upper right')  # Définir la position de la légende
        st.pyplot(plt)

    else:
        st.write("Aucune donnée à afficher pour les dépenses dans la sélection actuelle.")

    # ---- Ajout du Graphique en ligne (Line Plot) pour les dépenses ----
    if expense_type != "Aucun" and not filtered_df.empty:
        st.subheader(f"Graphique en ligne : Évolution des {expense_type} dans le Temps")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=filtered_df, x='Année', y=expense_type, hue='Institutions/Ministères', marker='o')
        plt.xticks(rotation=45)
        plt.title(f"Évolution des {expense_type} par Ministère")
        plt.ylabel(expense_type)
        plt.xlabel("Année")
        plt.legend(loc='upper right')  # Définir la position de la légende
        st.pyplot(plt)

    else:
        st.write("Aucune donnée à afficher pour le graphique en ligne des dépenses.")

    # ---- Ajout du Graphique à barres horizontales pour comparer les ministères ----
    st.subheader(f"Graphique à barres horizontales : Comparaison des ministères pour une année donnée")

    # Sélectionner une année spécifique pour la comparaison
    selected_year = st.selectbox('Sélectionnez une année pour comparer', options=sorted(df['Année'].unique()))

    # Filtrer les données pour l'année sélectionnée
    year_filtered_df = df[(df['Année'] == selected_year) & df['Institutions/Ministères'].isin(ministries)]

    if expense_type != "Aucun" and not year_filtered_df.empty:
        plt.figure(figsize=(10, 6))
        
        # Utiliser la palette qualitative 'Set1' pour des couleurs vives et distinctes
        sns.barplot(data=year_filtered_df, y='Institutions/Ministères', x=expense_type, 
                    hue='Institutions/Ministères', palette="Set1", dodge=False)
        plt.title(f"Comparaison des {expense_type} entre Ministères en {selected_year}")
        plt.xlabel(expense_type)
        plt.ylabel("Ministères")
        st.pyplot(plt)
    else:
        st.write(f"Aucune donnée disponible pour l'année sélectionnée ou les ministères.")
    
    # ---- Ajout du Graphique circulaire (Pie Chart) après le Graphique à barres horizontales ----
    st.subheader(f"Graphique circulaire : Répartition des {expense_type} pour l'année {selected_year}")
    
    if expense_type != "Aucun" and not year_filtered_df.empty:
        # Calculer la répartition des dépenses pour les ministères sélectionnés
        pie_data = year_filtered_df.groupby('Institutions/Ministères')[expense_type].sum()

        if not pie_data.empty and pie_data.sum() > 0:  # Vérification si les données existent et sont valides
            # Créer un graphique circulaire
            plt.figure(figsize=(8, 8))
            plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
            plt.title(f"Répartition des {expense_type} entre Ministères en {selected_year}")
            plt.axis('equal')  # Assure que le pie chart est circulaire
            st.pyplot(plt)
        else:
            st.write(f"Aucune donnée disponible pour générer le graphique circulaire pour l'année {selected_year}.")
    else:
        st.write(f"Aucune donnée disponible pour l'année {selected_year} ou les ministères sélectionnés.")
    
    # ---- Déplacer le Graphique en ligne pour l'indicateur ici (en bas) ----
    st.subheader(f"Graphique en ligne : Évolution de l'indicateur '{selected_indicator}' dans le Temps")
    
    if selected_indicator != "Aucun" and not filtered_df.empty:
        plt.figure(figsize=(10, 6))

        # Si aucun ministère n'est sélectionné, tracer le graphique sans 'hue' (légende ministères)
        if not ministries:
            sns.lineplot(data=filtered_df, x='Année', y=selected_indicator, marker='o')
            plt.title(f"Évolution de l'indicateur '{selected_indicator}'")
        else:
            sns.lineplot(data=filtered_df, x='Année', y=selected_indicator, hue='Institutions/Ministères', marker='o')
            plt.title(f"Évolution de l'indicateur '{selected_indicator}' par Ministère")
            plt.legend(loc='upper right')  # Définir la position de la légende

        plt.xticks(rotation=45)
        plt.ylabel(selected_indicator)
        plt.xlabel("Année")
        st.pyplot(plt)
    else:
        st.write(f"Aucune donnée à afficher pour l'indicateur '{selected_indicator}' dans la sélection actuelle.")
