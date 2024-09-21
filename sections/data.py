import streamlit as st
import pandas as pd
from io import BytesIO

def app(df):
    st.header('Données')
    st.write('Visualisez et explorez les données brutes ici.')

    # Forcer les colonnes de type chaîne de caractères à être de type string
    df['Institutions/Ministères'] = df['Institutions/Ministères'].astype(str)
    df['Année'] = df['Année'].astype(int)  # S'assurer que la colonne 'Année' est bien de type entier

    # Filtrage des données
    st.subheader('Filtrage des Données')
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))

    # Sélectionner entre "Budget Dépense Courante" et "Exécution Dépense"
    expense_type = st.selectbox("Sélectionnez un type de dépense", ["Budget Dépense Courante", "Exécution Dépense"])

    # Afficher uniquement les ministères qui ont des données dans la colonne sélectionnée
    available_ministries = df[df[expense_type].notna()]['Institutions/Ministères'].unique()
    ministry = st.selectbox(f"Sélectionnez un ministère pour {expense_type}", options=available_ministries)

    # Récupérer les 10 dernières colonnes comme indicateurs
    indicators_columns = df.columns[-10:]
    indicator = st.selectbox('Sélectionnez un indicateur', options=indicators_columns)

    # Appliquer les filtres
    filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
    if ministry:
        filtered_df = filtered_df[filtered_df['Institutions/Ministères'] == ministry]

    if indicator:
        st.subheader(f'Données pour l\'indicateur: {indicator}')

        # Première ligne : Année
        years_list = filtered_df['Année'].values
        # Deuxième ligne : Valeurs de l'indicateur
        indicator_values = filtered_df[indicator].values
        # Troisième ligne : Valeurs des dépenses
        expense_values = filtered_df[expense_type].values

        # Créer un DataFrame avec les années, l'indicateur, et le ministère
        data_for_display = pd.DataFrame({
            'Année': years_list,
            indicator: indicator_values,
            ministry: expense_values
        })

        # Transposer les données pour avoir un affichage plus clair
        data_for_display_transposed = data_for_display.T

        # Supprimer l'en-tête des colonnes (désactivation des noms des colonnes transposées)
        data_for_display_transposed.columns = [int(year) for year in years_list]  # Utiliser les années entières sans décimales
        data_for_display_transposed = data_for_display_transposed.drop(data_for_display_transposed.index[0])

        # Appliquer le style uniquement sur la première ligne (les années) pour les mettre en gras
        styled_df = data_for_display_transposed.style.applymap(
            lambda x: 'font-weight: bold', subset=pd.IndexSlice[:, data_for_display_transposed.columns]
        )

        # Afficher le tableau avec le style appliqué
        st.dataframe(styled_df)

        # Section de téléchargement pour "Données pour l'indicateur"
        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>Télécharger</h3>", unsafe_allow_html=True)

        @st.cache_data
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        @st.cache_data
        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        csv_indicator = convert_df_to_csv(data_for_display_transposed)
        excel_indicator = convert_df_to_excel(data_for_display_transposed)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="CSV",
                data=csv_indicator,
                file_name='donnees_indicateur.csv',
                mime='text/csv',
            )

        with col2:
            st.download_button(
                label="EXCEL",
                data=excel_indicator,
                file_name='donnees_indicateur.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

    # Affichage des Données Filtrées
    st.subheader('Données Filtrées')
    st.write(filtered_df)

    # Section de téléchargement pour "Données Filtrées"
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Télécharger</h3>", unsafe_allow_html=True)

    csv_filtered = convert_df_to_csv(filtered_df)
    excel_filtered = convert_df_to_excel(filtered_df)

    col3, col4 = st.columns(2)

    with col3:
        st.download_button(
            label="CSV",
            data=csv_filtered,
            file_name='donnees_filtrees.csv',
            mime='text/csv',
        )

    with col4:
        st.download_button(
            label="EXCEL",
            data=excel_filtered,
            file_name='donnees_filtrees.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )







