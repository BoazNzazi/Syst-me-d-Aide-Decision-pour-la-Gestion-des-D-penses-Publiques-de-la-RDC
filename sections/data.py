import streamlit as st
import pandas as pd
from io import BytesIO

def convert_to_csv(data):
    return data.to_csv().encode('utf-8')

def convert_to_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer)
    return output.getvalue()

def app(df):
    # Style CSS mis à jour
    st.markdown("""
    <style>
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
        .sub-header {
            text-align: center;
            padding: 10px;
            background-color: #f8f9fa;
            color: #004080;
            font-size: 18px;
            font-weight: bold;
            border-bottom: 4px solid #ddd;
            font-family: 'Arial', sans-serif;
        }
        .download-section {
            text-align: center;
            margin-top: 20px;
        }
        .download-section h4 {
            font-size: 16px;
            font-weight: bold;
            color: white; /* Texte en blanc */
            margin-bottom: 10px;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 15px; /* Espacement entre les boutons */
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            font-size: 16px; /* Taille de la police uniforme */
            font-weight: bold;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #0056b3;
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

    # Ajouter un espace entre l'en-tête et la section suivante
    st.markdown("<br>", unsafe_allow_html=True)

    # Préparer les données
    df['Institutions/Ministères'] = df['Institutions/Ministères'].astype(str)
    df['Année'] = df['Année'].astype(int)

    # Sélection de la plage d'années
    st.subheader('Données : Explorez les données brutes ici :')
    min_year, max_year = int(df['Année'].min()), int(df['Année'].max())
    years = st.slider('Sélectionnez la plage de dates', min_year, max_year, (min_year, max_year))

    # Tableau 1 : Ministère + Indicateur
    st.subheader('Tableau 1 : Ministère et Indicateur Sélectionnés')
    expense_type = st.selectbox(
        "Sélectionnez un type de dépense",
        options=["Choose an option", "Budget Dépense Courante", "Exécution Dépense"],
        index=0
    )

    if expense_type != "Choose an option":
        available_ministries = df[df[expense_type].notna()]['Institutions/Ministères'].unique()
        ministry = st.selectbox(f"Sélectionnez un ministère pour {expense_type}", options=["Choose an option"] + list(available_ministries))

        if ministry != "Choose an option":
            indicators_columns = df.columns[-10:]
            indicator = st.selectbox('Sélectionnez un indicateur', options=["Choose an option"] + list(indicators_columns))

            if indicator != "Choose an option":
                filtered_df = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
                ministry_data = filtered_df[filtered_df['Institutions/Ministères'] == ministry]

                # Construction du tableau avec années en colonnes
                table_data = pd.DataFrame(
                    {
                        "Années": filtered_df['Année'].unique(),
                        ministry: ministry_data.groupby('Année')[expense_type].sum(),
                        indicator: ministry_data.groupby('Année')[indicator].sum()
                    }
                ).set_index("Années").T

                st.write(f"### {ministry} : {indicator}")
                st.write(table_data)

                # Section de téléchargement
                st.markdown("""
                <div class='download-section'>
                    <h4>Télécharger</h4>
                    <div class='button-row'>
                """, unsafe_allow_html=True)

                # Boutons de téléchargement
                csv_table_data = convert_to_csv(table_data)
                excel_table_data = convert_to_excel(table_data)

                st.download_button("CSV", csv_table_data, "tableau.csv", "text/csv")
                st.download_button("Excel", excel_table_data, "tableau.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Tableau 2 : Données par Ministères/Institutions
    st.subheader('Tableau 2 : Données par Ministères/Institutions')
    if expense_type != "Choose an option":
        selected_ministries = st.multiselect(
            f"Sélectionnez un ou plusieurs ministères pour {expense_type}",
            options=available_ministries
        )

        if selected_ministries:
            ministry_table = df[
                (df['Année'] >= years[0]) & 
                (df['Année'] <= years[1]) & 
                (df['Institutions/Ministères'].isin(selected_ministries))
            ].pivot_table(
                index='Institutions/Ministères', 
                columns='Année', 
                values=expense_type, 
                aggfunc='sum'
            )
            st.write(ministry_table)

            # Section de téléchargement
            st.markdown("""
            <div class='download-section'>
                <h4>Télécharger</h4>
                <div class='button-row'>
            """, unsafe_allow_html=True)

            csv_ministry_table = convert_to_csv(ministry_table)
            excel_ministry_table = convert_to_excel(ministry_table)

            st.download_button("CSV", csv_ministry_table, "ministry_table.csv", "text/csv")
            st.download_button("Excel", excel_ministry_table, "ministry_table.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Tableau 3 : Données par Indicateurs
    st.subheader('Tableau 3 : Données par Indicateurs')
    indicators_columns = df.columns[-10:]
    selected_indicators = st.multiselect('Sélectionnez un ou plusieurs indicateurs', options=indicators_columns)

    if selected_indicators:
        indicator_table = df[
            (df['Année'] >= years[0]) & 
            (df['Année'] <= years[1])
        ][['Année'] + selected_indicators].pivot_table(
            index='Année', 
            aggfunc='sum'
        ).T

        st.write(indicator_table)

        # Section de téléchargement
        st.markdown("""
        <div class='download-section'>
            <h4>Télécharger</h4>
            <div class='button-row'>
        """, unsafe_allow_html=True)

        csv_indicator_table = convert_to_csv(indicator_table)
        excel_indicator_table = convert_to_excel(indicator_table)

        st.download_button("CSV", csv_indicator_table, "indicator_table.csv", "text/csv")
        st.download_button("Excel", excel_indicator_table, "indicator_table.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("---")