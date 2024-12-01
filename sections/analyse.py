import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import waterfall_chart
import warnings
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from fpdf import FPDF  # Import pour la génération de rapports PDF
import os  # Pour gérer les fichiers temporaires

# Ignorer les warnings FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# Couleur bleu ciel utilisée pour les montants
BLEU_CIEL = "#00BFFF"

# Fonction pour télécharger le graphique sous forme d'image
def download_plot_as_image(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Fonction pour générer un rapport PDF
def generate_pdf_report(ministry, year, budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage, conclusion):
    pdf = FPDF()
    pdf.add_page()

    # Titre du rapport
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=f"Rapport Budgétaire - {ministry} (Année {year})", ln=True, align='C')

    # Introduction
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Ce rapport présente une comparaison entre le budget alloué et le budget exécuté pour le ministère {ministry} durant l'année {year}.")

    # Détails des montants
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Détails des montants", ln=True)

    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"- Budget Alloué : {budget_alloue:.2f} millions de CDF", ln=True)
    pdf.cell(200, 10, txt=f"- Budget Exécuté : {budget_execute:.2f} millions de CDF", ln=True)
    pdf.cell(200, 10, txt=f"- Écart Absolu : {ecart_absolu:.2f} millions de CDF", ln=True)
    pdf.cell(200, 10, txt=f"- Écart en Pourcentage : {ecart_pourcentage:.2f}%", ln=True)

    # Analyse des écarts
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Analyse des Écarts", ln=True)

    pdf.set_font('Arial', '', 12)
    if ecart_absolu > 0:
        pdf.multi_cell(0, 10, txt="Le ministère n'a pas dépensé la totalité de son budget. Cela pourrait indiquer une sous-utilisation des ressources, nécessitant une meilleure planification.")
    elif ecart_absolu < 0:
        pdf.multi_cell(0, 10, txt="Le ministère a dépassé le budget alloué. Cela pourrait signaler des imprévus ou un manque de planification budgétaire.")
    else:
        pdf.multi_cell(0, 10, txt="Le ministère a bien géré son budget, en respectant le montant alloué.")

    # Conclusion
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Conclusion", ln=True)

    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, txt=conclusion)

    # Sauvegarder le PDF dans un fichier temporaire
    output_file = f"rapport_{ministry}_{year}.pdf"
    pdf.output(output_file)

    return output_file

def app(df):
    # En-tête avec "République Démocratique du Congo"
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #007bff; color: white;'>
        <h2 style='margin: 0;'>République Démocratique du Congo</h2>
    </div>
    """, unsafe_allow_html=True)

    # Nouvelle barre de navigation sans "À Propos", "Notre Mission", "Documentation"
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

    # Titre pour l'analyse avancée sans fond coloré
    st.markdown("""
    <div style='text-align: center; padding: 10px; color: #4CAF50;'>
        <h2 style='margin: 0;'>Analyse Avancée</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- Utilisation d'onglets pour organiser les graphiques ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Comparaison", "Statistiques", "Régression Linéaire", "Régression Multivariée", 
         "Segmentation", "Séries Temporelles"]
    )

    # Onglet Comparaison
    with tab1:
        st.markdown("<h4 style='color:#4CAF50;'>Comparaison Budget et Exécution</h4>", unsafe_allow_html=True)
        
        # Ajouter une option : Budget et Exécution
        options = ['Aucun ministère', 'Budget et Exécution'] + list(df['Institutions/Ministères'].unique())
        choix = st.selectbox("Sélectionnez une option ou un ministère", options)
        
        # Sélection de l'année avec un slider
        annee = st.slider(
            "Sélectionnez une année",
            int(df['Année'].min()),  # Année minimum
            int(df['Année'].max()),  # Année maximum
            step=1,  # Incrément par année
            value=int(df['Année'].min())  # Année par défaut
        )

        # Fonction pour afficher les montants et écarts avec style
        def afficher_montants(budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage):
            # Montant total affiché en bleu ciel
            st.markdown(f"<h5>Montant total pour l'année <span style='color:{BLEU_CIEL};'>{annee}</span></h5>", unsafe_allow_html=True)
            st.markdown(f"<b>Budget alloué</b> : <span style='color:{BLEU_CIEL};'>{budget_alloue:.2f} millions de CDF</span>", unsafe_allow_html=True)
            st.markdown(f"<b>Budget exécuté</b> : <span style='color:{BLEU_CIEL};'>{budget_execute:.2f} millions de CDF</span>", unsafe_allow_html=True)
            
            # Écart affiché en bleu ciel si positif, rouge si négatif
            ecart_color = BLEU_CIEL if ecart_absolu >= 0 else "red"
            st.markdown(f"<b>Écart absolu</b> : <span style='color:{ecart_color};'>{ecart_absolu:.2f} millions de CDF</span>", unsafe_allow_html=True)
            st.markdown(f"<b>Écart en pourcentage</b> : <span style='color:{ecart_color};'>{ecart_pourcentage:.2f}%</span>", unsafe_allow_html=True)

        # Fonction pour générer un rapport PDF
        def generer_rapport_pdf(choix, annee, budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage):
            conclusion = "Le ministère a bien géré son budget global avec une légère sous-utilisation des fonds." if ecart_absolu > 0 else "Le ministère a dépassé son budget alloué."
            pdf_file = generate_pdf_report(choix, annee, budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage, conclusion)

            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Télécharger le rapport PDF",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

            os.remove(pdf_file)

        # Affichage conditionnel selon le choix de l'utilisateur
        if choix == 'Aucun ministère':
            st.warning("Veuillez sélectionner une option ou un ministère pour continuer.")
        
        # Si "Budget et Exécution" est choisi
        elif choix == 'Budget et Exécution':
            df_filtered = df[df['Année'] == annee].fillna(0)
            
            # Calcul du total des budgets
            total_budget_alloue = df_filtered['Budget Dépense Courante'].sum()
            total_budget_execute = df_filtered['Exécution Dépense'].sum()

            # Calcul de l'écart
            ecart_absolu = total_budget_alloue - total_budget_execute
            ecart_pourcentage = (ecart_absolu / total_budget_alloue) * 100 if total_budget_alloue != 0 else 0
            
            # Afficher les montants et écarts
            afficher_montants(total_budget_alloue, total_budget_execute, ecart_absolu, ecart_pourcentage)

            # Générer et télécharger le rapport PDF
            generer_rapport_pdf("Budget et Exécution", annee, total_budget_alloue, total_budget_execute, ecart_absolu, ecart_pourcentage)

            # Barre de progression pour imiter le chargement des graphiques
            st.markdown("**Génération des graphiques...**")
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            # --- Premier Graphique : Bar Plot ---
            st.subheader("Graphique Bar Plot")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(['Budget Alloué', 'Budget Exécuté'], [total_budget_alloue, total_budget_execute], color=['#4682B4', '#32CD32'])
            ax.set_title(f"Comparaison du Budget Alloué et Exécuté pour l'année {annee}")
            ax.set_ylabel("Montant en millions de CDF")
            st.pyplot(fig)

            st.download_button(
                label="Télécharger le graphique (Bar Plot)",
                data=download_plot_as_image(fig),
                file_name=f"comparaison_budget_{annee}.png",
                mime="image/png"
            )
            
            # --- Deuxième Graphique : Pie Chart pour comparaison ---
            if total_budget_alloue != 0 or total_budget_execute != 0:
                st.subheader("Comparaison en pourcentage (Graphique en secteurs)")
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                labels = ['Budget Alloué', 'Budget Exécuté']
                sizes = [total_budget_alloue, total_budget_execute]
                ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4682B4', '#32CD32'])
                ax2.axis('equal')  # Pour que le pie chart soit circulaire
                ax2.set_title(f"Répartition des budgets pour l'année {annee}")
                st.pyplot(fig2)

                st.download_button(
                    label="Télécharger le graphique (Pie Chart)",
                    data=download_plot_as_image(fig2),
                    file_name=f"comparaison_pie_budget_{annee}.png",
                    mime="image/png"
                )
            else:
                st.warning("Les montants alloués et exécutés sont nuls, aucun graphique en secteurs ne peut être généré.")

            # --- Troisième Graphique : Waterfall Chart ---
                     # --- Troisième Graphique : Waterfall Chart ---
            st.subheader("Comparaison avec Waterfall Chart")

            data = [total_budget_alloue, -ecart_absolu]
            labels = ['Budget Alloué', 'Écart (Budget non utilisé)']

            fig3, ax3 = plt.subplots(figsize=(6, 4))
            waterfall_chart.plot(labels, data)
            ax3.set_ylim(0, 3000000)  # Fixe l'axe y à une plage constante (ajustez selon vos données)
            plt.title(f"Waterfall Chart pour l'année {annee}")
            plt.ylabel("Montant en millions de CDF")
            st.pyplot(plt)

            st.download_button(
                label="Télécharger le graphique (Waterfall Chart)",
                data=download_plot_as_image(fig3),
                file_name=f"comparaison_waterfall_budget_{annee}.png",
                mime="image/png"
            )

        # Si un ministère est sélectionné
        else:
            df_filtered = df[(df['Institutions/Ministères'] == choix) & (df['Année'] == annee)].fillna(0)
            
            if not df_filtered.empty:
                budget_alloue = df_filtered['Budget Dépense Courante'].values[0]
                budget_execute = df_filtered['Exécution Dépense'].values[0]

                if budget_alloue == 0 and budget_execute == 0:
                    st.warning("Aucune donnée valide n'est disponible pour cette année et ce ministère.")
                else:
                    # Calcul de l'écart
                    ecart_absolu = budget_alloue - budget_execute
                    ecart_pourcentage = (ecart_absolu / budget_alloue) * 100 if budget_alloue != 0 else 0
                    
                    # Afficher les montants et écarts
                    afficher_montants(budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage)
                    
                    # Générer et télécharger le rapport PDF
                    generer_rapport_pdf(choix, annee, budget_alloue, budget_execute, ecart_absolu, ecart_pourcentage)

                    # Graphiques restants...

                    # --- Premier Graphique : Bar Plot ---
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.bar(['Budget Alloué', 'Budget Exécuté'], [budget_alloue, budget_execute], color=['#4682B4', '#32CD32'])
                    ax.set_title(f"Comparaison des budgets pour {choix} en {annee}")
                    ax.set_ylabel("Montant en millions de CDF")
                    st.pyplot(fig)
                    
                    st.download_button(
                        label="Télécharger le graphique (Bar Plot)",
                        data=download_plot_as_image(fig),
                        file_name=f"comparaison_{choix.replace(' ', '_')}_{annee}.png",
                        mime="image/png"
                    )
                    
                    # --- Deuxième Graphique : Pie Chart pour comparaison ---
                    st.subheader("Comparaison en pourcentage (Graphique en secteurs)")
                    fig2, ax2 = plt.subplots(figsize=(6, 4))
                    labels = ['Budget Alloué', 'Budget Exécuté']
                    sizes = [budget_alloue, budget_execute]
                    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#4682B4', '#32CD32'])
                    ax2.axis('equal')  # Pour que le pie chart soit circulaire
                    ax2.set_title(f"Répartition des budgets pour {choix} en {annee}")
                    st.pyplot(fig2)

                    st.download_button(
                        label="Télécharger le graphique (Pie Chart)",
                        data=download_plot_as_image(fig2),
                        file_name=f"comparaison_pie_{choix.replace(' ', '_')}_{annee}.png",
                        mime="image/png"
                    )

                    # --- Troisième Graphique : Waterfall Chart ---
                    st.subheader("Comparaison avec Waterfall Chart")
                    try:
                        data = [budget_alloue, -ecart_absolu]
                        labels = ['Budget Alloué', 'Écart (Budget non utilisé)']

                        fig3, ax3 = plt.subplots(figsize=(6, 4))
                        waterfall_chart.plot(labels, data, ax=ax3)
                        ax3.set_ylim(min(data) - 500000, max(data) + 500000)  # Fixe l'axe y à une plage constante
                        ax3.set_title(f"Waterfall Chart pour {choix} en {annee}")
                        ax3.set_ylabel("Montant en millions de CDF")
                        st.pyplot(fig3)

                        st.download_button(
                            label="Télécharger le graphique (Waterfall Chart)",
                            data=download_plot_as_image(fig3),
                            file_name=f"comparaison_waterfall_{choix.replace(' ', '_')}_{annee}.png",
                            mime="image/png"
                        )
                    except Exception as e:
                        st.error(f"Erreur lors de la génération du Waterfall Chart : {e}")
            else:
                st.write(f"Aucune donnée disponible pour {choix} en {annee}")
    # Onglet Statistiques
    with tab2:
        st.markdown("<h4 style='color:#607D8B;'>Statistiques Descriptives</h4>", unsafe_allow_html=True)
        
        # Sélection de la plage d'années pour filtrer les données
        st.markdown("<h6 style='color:#B0BEC5;'>Sélectionnez une plage d'années pour calculer les statistiques :</h6>", unsafe_allow_html=True)
        min_year = int(df['Année'].min())
        max_year = int(df['Année'].max())
        annee_range = st.slider("Sélectionnez la plage d'années", min_year, max_year, (min_year, max_year), key="slider_annee_statistique")

        # Filtrer les données selon la plage d'années sélectionnée
        df_filtered = df[(df['Année'] >= annee_range[0]) & (df['Année'] <= annee_range[1])]

        # Sélection des variables (colonnes) pour calculer les statistiques
        st.markdown("<h6 style='color:#B0BEC5;'>Sélectionnez les variables pour afficher les statistiques :</h6>", unsafe_allow_html=True)
        variable_options = df.columns.tolist()
        variables_choisies = st.multiselect("Choisissez les variables", variable_options, default=None)

        # Si des variables sont sélectionnées, calculer les statistiques descriptives
        if len(variables_choisies) > 0:
            st.write("Résumé statistique des données pour la période sélectionnée :")
            st.write(df_filtered[variables_choisies].describe())
        else:
            st.warning("Veuillez sélectionner au moins une variable pour afficher les statistiques descriptives.")
        
        # Option pour afficher la distribution des dépenses
        if st.checkbox("Afficher la distribution des dépenses par année"):
            # Filtrer les données uniquement pour les variables sélectionnées
            fig = sns.pairplot(df_filtered[variables_choisies], diag_kind='kde')
            st.pyplot(fig)

            
    # Onglet Régression Linéaire
    with tab3:
        st.markdown("<h4 style='color:#4CAF50; text-align:center;'>Régression Linéaire</h4>", unsafe_allow_html=True)

        # Sélection de la plage d'années
        st.markdown("<h6 style='color:#4CAF50;'>Sélectionnez une plage d'années pour l'analyse régressive :</h6>", unsafe_allow_html=True)
        min_year = int(df['Année'].min())
        max_year = int(df['Année'].max())
        annee_range = st.slider("Sélectionnez la plage d'années", min_year, max_year, (min_year, max_year))

        # Sélection du ministère (variable indépendante)
        ministere_options = ['Aucun ministère'] + list(df['Institutions/Ministères'].unique())
        ministere_choix = st.selectbox("Choisissez un ministère (variable indépendante)", ministere_options, key="ministere_choix_lineaire")

        # Sélection de l'indicateur (variable dépendante)
        indicateur_options = ['Aucun indicateur'] + [col for col in df.columns if col not in ['Institutions/Ministères', 'Année', 'Budget Dépense Courante', 'Exécution Dépense']]
        indicateur_choix = st.selectbox("Choisissez un indicateur (variable dépendante)", indicateur_options, key="indicateur_choix_lineaire")

        # Si aucun ministère ou indicateur n'est sélectionné
        if ministere_choix == 'Aucun ministère' or indicateur_choix == 'Aucun indicateur':
            st.warning("Veuillez sélectionner à la fois un ministère et un indicateur pour continuer l'analyse.")
        else:
            # Filtrer les données par plage d'années et ministère
            df_ministere = df[(df['Institutions/Ministères'] == ministere_choix) & 
                            (df['Année'] >= annee_range[0]) & 
                            (df['Année'] <= annee_range[1])]

            # Extraction des variables X (dépenses) et y (indicateur économique)
            X = df_ministere[['Budget Dépense Courante']].fillna(0)
            y = df_ministere[indicateur_choix].fillna(0)

            # Vérifier s'il y a suffisamment de données pour faire une régression
            if len(X) > 1 and len(y) > 1:
                # Division des données en ensembles d'entraînement et de test
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Création et ajustement du modèle de régression linéaire
                model = LinearRegression()
                model.fit(X_train, y_train)

                # Prédiction sur les données de test
                y_pred = model.predict(X_test)

                # Affichage du graphique de régression
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.scatter(X_test, y_test, color='blue', label='Valeurs réelles')
                ax.plot(X_test, y_pred, color='red', label='Prédictions')
                ax.set_title(f"Régression Linéaire : {ministere_choix} vs {indicateur_choix}")
                ax.set_xlabel(f'Dépenses du ministère ({ministere_choix})')
                ax.set_ylabel(indicateur_choix)
                ax.legend()
                st.pyplot(fig)

                # Affichage des coefficients de régression
                coef = model.coef_[0]
                intercept = model.intercept_
                r2_score = model.score(X_test, y_test)
                st.write(f"**Coefficient de régression (pente)** : {coef:.4f}")
                st.write(f"**Ordonnée à l'origine** : {intercept:.4f}")
                st.write(f"**R² (Score de détermination)** : {r2_score:.4f}")

                # Téléchargement du graphique
                st.download_button(
                    label="Télécharger le graphique (Régression Linéaire)",
                    data=download_plot_as_image(fig),
                    file_name=f"regression_lineaire_{ministere_choix}_{indicateur_choix}.png",
                    mime="image/png"
                )

                # --- Générer le rapport PDF après l'analyse rétrospective ---
                # --- Générer le rapport PDF après l'analyse rétrospective ---
                def generate_regression_report_pdf(ministere_choix, indicateur_choix, coef, intercept, r2_score, annee_range):
                    # Nettoyage du texte pour le nom du fichier
                    safe_ministere = ministere_choix.replace("/", "_").replace("\\", "_").replace(" ", "_")
                    safe_indicateur = indicateur_choix.replace("/", "_").replace("\\", "_").replace(" ", "_")

                    pdf = FPDF()
                    pdf.add_page()

                    # Titre du rapport
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(200, 10, txt=f"Rapport Régression Linéaire : {ministere_choix} (Indicateur : {indicateur_choix})", ln=True, align='C')

                    # Introduction et Objectif de l'analyse
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Introduction et Objectif de l'Analyse", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(10)
                    pdf.multi_cell(0, 10, txt=(
                        f"Cette analyse rétrospective couvre les années {annee_range[0]} à {annee_range[1]} pour comprendre l'impact des dépenses du ministère {ministere_choix} "
                        f"sur l'indicateur économique {indicateur_choix}. En utilisant une régression linéaire, cette analyse vise à établir une relation mathématique entre les "
                        f"variations des dépenses et leur impact sur l'indicateur {indicateur_choix}, afin d'aider à la prise de décision pour les futures allocations budgétaires."
                    ))

                    # Détails de l'équation de la régression linéaire
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Équation de la régression linéaire", ln=True)
                    pdf.set_font('Arial', 'I', 12)
                    pdf.ln(5)
                    pdf.multi_cell(0, 10, txt=(
                        f"*{indicateur_choix}* = **{coef:.4f}** * Dépenses_{ministere_choix} + **{intercept:.4f}**\n\n"
                        f"- Coefficient de régression (pente) : {coef:.4f}\n"
                        f"- Ordonnée à l'origine : {intercept:.4f}\n"
                        f"- Score de détermination (R²) : {r2_score:.4f}"
                    ))

                    # Détails des résultats de la régression
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Analyse et Interprétations de Résultat", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(5)

                    # Interprétation intelligente basée sur les valeurs des coefficients et R²
                    if coef > 0 and r2_score > 0:
                        pdf.multi_cell(0, 10, txt=(
                            f"Avec ces résultats, la corrélation semble positive :\n\n"
                            f"- **Coefficient de régression (pente)** : {coef:.4f}\n"
                            f"Un coefficient de régression positif signifie qu'il y a une relation directe entre les dépenses du ministère et l'indicateur {indicateur_choix}. "
                            f"Une augmentation des dépenses semble entraîner une augmentation de l'indicateur {indicateur_choix}.\n\n"
                            f"- **Ordonnée à l'origine** : {intercept:.4f}\n"
                            f"L'ordonnée à l'origine représente la valeur estimée de l'indicateur {indicateur_choix} lorsque les dépenses du ministère sont égales à zéro.\n\n"
                            f"- **Score de détermination (R²)** : {r2_score:.4f}\n"
                            f"Un score R² de {r2_score:.4f} montre une corrélation modérée. Cela signifie que {r2_score*100:.2f}% des variations de l'indicateur "
                            f"peuvent être expliquées par les variations des dépenses."
                        ))
                    elif coef < 0 and r2_score > 0:
                        pdf.multi_cell(0, 10, txt=(
                            f"Avec ces résultats, la corrélation semble négative :\n\n"
                            f"- **Coefficient de régression (pente)** : {coef:.4f}\n"
                            f"Un coefficient de régression négatif signifie qu'il existe une relation inverse entre les dépenses du ministère et l'indicateur {indicateur_choix}. "
                            f"Autrement dit, une augmentation des dépenses est associée à une diminution de l'indicateur {indicateur_choix}.\n\n"
                            f"- **Ordonnée à l'origine** : {intercept:.4f}\n"
                            f"L'ordonnée à l'origine représente la valeur estimée de l'indicateur {indicateur_choix} lorsque les dépenses du ministère sont égales à zéro.\n\n"
                            f"- **Score de détermination (R²)** : {r2_score:.4f}\n"
                            f"Un score R² de {r2_score:.4f} montre que {r2_score*100:.2f}% des variations de l'indicateur peuvent être expliquées par les variations des dépenses."
                        ))
                    else:
                        pdf.multi_cell(0, 10, txt=(
                            f"Avec ces résultats, la corrélation est mauvaise :\n\n"
                            f"- **Coefficient de régression (pente)** : {coef:.4f}\n"
                            f"Un coefficient de régression proche de 0 signifie qu'il n'y a pratiquement pas de relation entre les dépenses du ministère et l'indicateur {indicateur_choix}.\n\n"
                            f"- **Ordonnée à l'origine** : {intercept:.4f}\n"
                            f"L'ordonnée à l'origine représente la valeur estimée de l'indicateur {indicateur_choix} lorsque les dépenses du ministère sont égales à zéro.\n\n"
                            f"- **Score de détermination (R²)** : {r2_score:.4f}\n"
                            f"Un score R² négatif de {r2_score:.4f} indique que le modèle de régression linéaire est moins performant qu'une simple moyenne pour prédire les valeurs de l'indicateur. "
                            f"Le modèle n'explique donc pas correctement les variations de l'indicateur en fonction des dépenses."
                        ))

                    # Conclusion et Recommandations
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Conclusion et Recommandations", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(5)
                    
                    if r2_score > 0:
                        pdf.multi_cell(0, 10, txt=(
                            f"La régression montre une relation entre les dépenses du ministère {ministere_choix} et l'indicateur {indicateur_choix}. "
                            f"Pour optimiser les futures allocations, il est recommandé d'augmenter les investissements dans ce secteur, car les dépenses ont montré "
                            f"un impact positif sur cet indicateur économique."
                        ))
                    elif coef < 0 and r2_score < 0:
                        pdf.multi_cell(0, 10, txt=(
                            f"Les résultats montrent une relation négative et un score R² faible entre les dépenses du ministère {ministere_choix} et l'indicateur {indicateur_choix}. "
                            f"Nous recommandons de ne pas trop investir dans ce secteur, car cela pourrait réduire son impact sur l'indicateur économique."
                        ))
                    else:
                        pdf.multi_cell(0, 10, txt=(
                            f"Les résultats montrent qu'il n'y a pas de lien significatif entre les dépenses du ministère {ministere_choix} et l'indicateur {indicateur_choix}. "
                            f"Le modèle de régression linéaire utilisé n'est pas adéquat pour expliquer les variations de cet indicateur. "
                            f"Il serait recommandé d'explorer d'autres variables ou d'utiliser des méthodes plus complexes pour mieux comprendre les facteurs influençant cet indicateur."
                        ))

                    # Sauvegarder le PDF dans un fichier temporaire
                    output_file = f"rapport_regression_{safe_ministere}_{safe_indicateur}.pdf"
                    pdf.output(output_file)

                    return output_file

            if len(df) >= 2:

                # Génération du rapport PDF après l'analyse
                pdf_file = generate_regression_report_pdf(ministere_choix, indicateur_choix, coef, intercept, r2_score, annee_range)

                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="Télécharger le rapport PDF (Régression Linéaire)",
                        data=file,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

                os.remove(pdf_file)  # Supprimer le fichier PDF après téléchargement

            else:
                st.warning("Pas assez de données pour effectuer une régression linéaire.")

    with tab4:
        st.markdown("<h4 style='color:#4CAF50;'>Régression Multivariée</h4>", unsafe_allow_html=True)

        # Sélection de la plage d'années avec une clé unique
        st.markdown("<h6 style='color:#4CAF50;'>Sélectionnez une plage d'années pour l'analyse régressive :</h6>", unsafe_allow_html=True)
        min_year = int(df['Année'].min())
        max_year = int(df['Année'].max())
        annee_range = st.slider("Sélectionnez la plage d'années", min_year, max_year, (min_year, max_year), key="slider_annee_multivariee")

        # Sélection des ministères (variables indépendantes)
        ministere_options = list(df['Institutions/Ministères'].unique())
        ministere_choix = st.multiselect("Choisissez 2 ministères ou plus (variables indépendantes)", ministere_options)

        # Sélection de l'indicateur (variable dépendante)
        indicateur_options = [col for col in df.columns if col not in ['Institutions/Ministères', 'Année', 'Budget Dépense Courante', 'Exécution Dépense']]
        indicateur_choix = st.selectbox("Choisissez un indicateur (variable dépendante)", indicateur_options)

        # Vérifier si au moins deux ministères ont été sélectionnés
        if len(ministere_choix) >= 2:
            # Filtrer les données pour les ministères sélectionnés et plage d'années
            df_selected = df[(df['Institutions/Ministères'].isin(ministere_choix)) & 
                            (df['Année'] >= annee_range[0]) & 
                            (df['Année'] <= annee_range[1])]

            # Ajouter une colonne 'Total Dépenses' pour combiner les budgets des ministères sélectionnés
            df_selected = df_selected.groupby('Année').sum().reset_index()

            # Extraction des variables indépendantes (total des budgets des ministères sélectionnés)
            X = df_selected[['Budget Dépense Courante', 'Exécution Dépense']].fillna(0)

            # Variable dépendante
            y = df_selected[indicateur_choix].fillna(0)

            # Vérifier s'il y a suffisamment de données pour faire une régression
            if len(X) > 1 and len(y) > 1:
                # Division des données en ensembles d'entraînement et de test
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Création et ajustement du modèle de régression multivariée
                model = LinearRegression()
                model.fit(X_train, y_train)

                # Prédiction sur les données de test
                y_pred = model.predict(X_test)

                # Affichage des coefficients de régression
                coef = model.coef_
                intercept = model.intercept_
                st.write(f"**Coefficients des variables indépendantes** : {coef}")
                st.write(f"**Ordonnée à l'origine** : {intercept}")

                # Évaluation du modèle
                r2_score = model.score(X_test, y_test)
                st.write(f"**R² (Score de détermination)** : {r2_score:.4f}")

                # Affichage des résultats de la régression sous forme de graphique
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.scatter(y_test, y_pred, color='blue')
                ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
                ax.set_xlabel('Valeurs réelles')
                ax.set_ylabel('Prédictions')
                ax.set_title(f"Régression Multivariée : {ministere_choix} vs {indicateur_choix}")
                st.pyplot(fig)

                # Bouton de téléchargement du graphique
                st.download_button(
                    label="Télécharger le graphique (Régression Multivariée)",
                    data=download_plot_as_image(fig),
                    file_name=f"regression_multivariee_{ministere_choix}_{indicateur_choix}.png",
                    mime="image/png"
                )

                # --- Générer le rapport PDF après l'analyse rétrospective ---
                def generate_multivariate_regression_report_pdf(ministere_choix, indicateur_choix, coef, intercept, r2_score, annee_range):
                    # Nettoyage du texte pour le nom du fichier
                    safe_ministere = "_".join([m.replace("/", "_").replace("\\", "_").replace(" ", "_") for m in ministere_choix])
                    safe_indicateur = indicateur_choix.replace("/", "_").replace("\\", "_").replace(" ", "_")

                    pdf = FPDF()
                    pdf.add_page()

                    # Titre du rapport
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(200, 10, txt=f"Rapport Régression Multivariée : {ministere_choix} (Indicateur : {indicateur_choix})", ln=True, align='C')

                    # Introduction et Objectif de l'analyse
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Introduction et Objectif de l'Analyse", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(10)
                    pdf.multi_cell(0, 10, txt=(
                        f"Cette analyse rétrospective couvre les années {annee_range[0]} à {annee_range[1]} pour comprendre l'impact des dépenses des ministères {ministere_choix} "
                        f"sur l'indicateur économique {indicateur_choix}. En utilisant une régression multivariée, cette analyse vise à établir une relation mathématique entre les "
                        f"variations des dépenses cumulées et leur impact sur l'indicateur {indicateur_choix}, afin d'aider à la prise de décision pour les futures allocations budgétaires."
                    ))

                    # Détails de l'équation de la régression multivariée
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Équation de la régression multivariée", ln=True)
                    pdf.set_font('Arial', 'I', 12)
                    pdf.ln(5)
                    coef_str = " + ".join([f"({c:.4f} * Dépenses_{ministere_choix[i]})" for i, c in enumerate(coef)])
                    pdf.multi_cell(0, 10, txt=(
                        f"*{indicateur_choix}* = {coef_str} + {intercept:.4f}\n\n"
                        f"- Coefficients des ministères : {coef}\n"
                        f"- Ordonnée à l'origine : {intercept:.4f}\n"
                        f"- Score de détermination (R²) : {r2_score:.4f}"
                    ))

                    # Analyse et Interprétation de Résultats
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Analyse et Interprétations de Résultat", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(5)
                    
                    # Interprétation plus détaillée pour chaque coefficient et score R²
                    if r2_score > 0:
                        # Interprétation de chaque coefficient
                        for i, c in enumerate(coef):
                            if c > 0:
                                pdf.multi_cell(0, 10, txt=(
                                    f"- **Coefficient de régression pour {ministere_choix[i]}** : {c:.4f}\n"
                                    f"Un coefficient positif indique qu'une augmentation des dépenses de {ministere_choix[i]} est associée à une augmentation de l'indicateur {indicateur_choix}.\n\n"
                                ))
                            else:
                                pdf.multi_cell(0, 10, txt=(
                                    f"- **Coefficient de régression pour {ministere_choix[i]}** : {c:.4f}\n"
                                    f"Un coefficient négatif indique qu'une augmentation des dépenses de {ministere_choix[i]} est associée à une diminution de l'indicateur {indicateur_choix}.\n\n"
                                ))

                        # Interprétation globale du modèle
                        pdf.multi_cell(0, 10, txt=(
                            f"Le score de détermination R² de {r2_score:.4f} montre qu'environ {r2_score*100:.2f}% des variations de l'indicateur {indicateur_choix} "
                            f"peuvent être expliquées par les dépenses cumulées des ministères {ministere_choix}. Cela suggère que le modèle capture bien la relation entre les dépenses et l'indicateur."
                        ))
                    else:
                        # Interprétation pour un modèle avec R² négatif ou très faible
                        pdf.multi_cell(0, 10, txt=(
                            f"Les résultats montrent une corrélation faible ou inexistante entre les dépenses des ministères {ministere_choix} et l'indicateur {indicateur_choix}.\n"
                            f"- **Coefficients de régression** : {coef}\n"
                            f"Des coefficients proches de 0 indiquent qu'il n'y a pratiquement aucune relation entre les dépenses des ministères et l'indicateur {indicateur_choix}.\n\n"
                            f"- **Ordonnée à l'origine** : {intercept:.4f}\n"
                            f"L'ordonnée à l'origine représente la valeur estimée de l'indicateur {indicateur_choix} lorsque les dépenses des ministères sont égales à zéro.\n\n"
                            f"- **Score de détermination (R²)** : {r2_score:.4f}\n"
                            f"Un score R² négatif de {r2_score:.4f} indique que le modèle de régression multivariée n'est pas performant. Cela signifie que les dépenses des ministères sélectionnés "
                            f"n'expliquent pas correctement les variations de l'indicateur {indicateur_choix}."
                        ))

                    # Conclusion et Recommandations
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(200, 10, txt="Conclusion et Recommandations", ln=True)
                    pdf.set_font('Arial', '', 12)
                    pdf.ln(5)
                    
                    if r2_score > 0:
                        pdf.multi_cell(0, 10, txt=(
                            f"Cette analyse suggère que les dépenses cumulées des ministères {ministere_choix} ont un impact sur l'indicateur {indicateur_choix}. "
                            f"Pour optimiser les futures allocations budgétaires, il est recommandé de surveiller de près ces dépenses et d'ajuster les budgets en fonction des résultats observés."
                        ))
                    else:
                        pdf.multi_cell(0, 10, txt=(
                            f"Les résultats montrent qu'il n'y a pas de lien significatif entre les dépenses des ministères {ministere_choix} et l'indicateur {indicateur_choix}. "
                            f"Il est recommandé d'explorer d'autres facteurs ou indicateurs pour mieux comprendre les relations budgétaires et économiques."
                        ))

                    # Sauvegarder le PDF dans un fichier temporaire
                    output_file = f"rapport_regression_multivariee_{safe_ministere}_{safe_indicateur}.pdf"
                    pdf.output(output_file)

                    return output_file




                # Génération du rapport PDF après l'analyse
                pdf_file = generate_multivariate_regression_report_pdf(ministere_choix, indicateur_choix, coef, intercept, r2_score, annee_range)

                with open(pdf_file, "rb") as file:
                    st.download_button(
                        label="Télécharger le rapport PDF (Régression Multivariée)",
                        data=file,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

                os.remove(pdf_file)  # Supprimer le fichier PDF après téléchargement
            else:
                st.warning("Pas assez de données pour effectuer une régression multivariée.")
        else:
            st.warning("Veuillez sélectionner au moins 2 ministères pour effectuer une régression multivariée.")

        