import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import waterfall_chart
import warnings
import time

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

    # Titre pour l'analyse avancée
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: #4CAF50; color: white;'>
        <h2 style='margin: 0;'>Analyse Avancée</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- Utilisation d'onglets pour organiser les graphiques ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Comparaison", "Régression Linéaire", "Régressions Multivariées", 
         "Segmentation", "Random Forests", "Séries Temporelles"]
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
            
            # Barre de progression pour imiter le chargement des graphiques
            st.markdown("**Génération des graphiques...**")
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
            
            # --- Premier Graphique : Bar Plot ---
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
            st.subheader("Comparaison avec Waterfall Chart")

            data = [total_budget_alloue, -ecart_absolu]
            labels = ['Budget Alloué', 'Écart (Budget non utilisé)']

            fig3, ax3 = plt.subplots(figsize=(6, 4))
            waterfall_chart.plot(labels, data)
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
                    
                    # Barre de progression pour imiter le chargement des graphiques
                    st.markdown("**Génération des graphiques...**")
                    progress_bar = st.progress(0)
                    for percent_complete in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(percent_complete + 1)
                    
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

                    data = [budget_alloue, -ecart_absolu]
                    labels = ['Budget Alloué', 'Écart (Budget non utilisé)']

                    fig3, ax3 = plt.subplots(figsize=(6, 4))
                    waterfall_chart.plot(labels, data)
                    plt.title(f"Waterfall Chart pour {choix} en {annee}")
                    plt.ylabel("Montant en millions de CDF")
                    st.pyplot(plt)

                    st.download_button(
                        label="Télécharger le graphique (Waterfall Chart)",
                        data=download_plot_as_image(fig3),
                        file_name=f"comparaison_waterfall_{choix.replace(' ', '_')}_{annee}.png",
                        mime="image/png"
                    )
            
            else:
                st.write(f"Aucune donnée disponible pour {choix} en {annee}")








