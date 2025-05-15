import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO, BytesIO

# --- 1. Data Loading & Preparation ---
@st.cache_data
def load_data(file_path="Cadre Tunisie.csv"): # <--- MODIFIED HERE
    """Loads the CSV data into a pandas DataFrame."""
    try:
        # Attempt to load with utf-8 encoding first, common for diverse text data
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            # If utf-8 fails, try latin1, another common encoding
            st.warning(f"UTF-8 decoding failed for {file_path}. Trying 'latin1' encoding.")
            df = pd.read_csv(file_path, encoding='latin1')
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Make sure it's in the root directory of your GitHub repository along with your app.py.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the file '{file_path}': {e}")
        return None

# --- Helper function to make data downloadable ---
def to_csv(df_to_download):
    if isinstance(df_to_download.index, pd.MultiIndex):
        csv_data = df_to_download.reset_index().to_csv(index=False).encode('utf-8')
    elif df_to_download.index.name is not None or not isinstance(df_to_download.index, pd.RangeIndex):
         csv_data = df_to_download.reset_index().to_csv(index=False).encode('utf-8')
    else:
        csv_data = df_to_download.to_csv(index=False).encode('utf-8')
    return csv_data

# --- Main part of the Streamlit app ---
st.set_page_config(page_title="Application de Théorie de Sondage", layout="wide") # Optional: Set page config

st.title("Projet Théorie de Sondage")
st.subheader("Application pour le Tirage Automatique d'Échantillons")
st.markdown("---") # Adds a horizontal line

# --- INTRODUCTION SECTION ---
st.header("Bienvenue dans l'Application de Sondage")
st.markdown("""
Cette application a été développée dans le cadre du projet de Théorie de Sondage.
Elle permet aux utilisateurs de tirer automatiquement des échantillons à partir d'un cadre de sondage
basé sur les blocs du recensement Tunisien.

**Fonctionnalités Principales :**
1.  **Chargement de Données :** L'application charge un cadre de sondage prédéfini (`Cadre Tunisie.csv`).
2.  **Deux Méthodes d'Échantillonnage :**
    *   **SAS (Aléatoire Simple Sans Remise) :**
        *   Permet de sélectionner aléatoirement un nombre spécifié d'unités (blocs) du cadre, où chaque unité a une chance égale d'être choisie.
        *   Utile pour obtenir un aperçu général lorsque la population est supposée homogène.
        *   L'application fournit l'échantillon, des statistiques descriptives, et une comparaison (tableau et graphique) avec le cadre de sondage pour une variable choisie.
    *   **Stratifié (Allocation Proportionnelle) :**
        *   Divise la population en sous-groupes (strates) basés sur une variable de stratification choisie (Région, Gouvernorat, Délégation).
        *   Tire ensuite un échantillon de chaque strate proportionnellement à la taille de cette strate par rapport à la population totale (basée sur `pop_block`).
        *   Assure une meilleure représentation des différents sous-groupes dans l'échantillon.
        *   L'application fournit le tableau d'allocation, l'échantillon stratifié et ses statistiques descriptives.
3.  **Interactivité :** L'utilisateur peut spécifier la taille de l'échantillon et les variables pertinentes pour chaque méthode.
4.  **Téléchargement des Résultats :** Tous les tableaux et graphiques générés peuvent être téléchargés.

**Objectif du Projet :**
Développer une application permettant de tirer automatiquement un échantillon de taille *n* selon les méthodes SAS et Stratifiée à allocation proportionnelle.

**Base d'échantillonnage :** Cadre d'échantillonnage basé sur la division du territoire Tunisien en blocs conçus à partir du dernier recensement général de la population. Chaque bloc représente une unité géographique relativement homogène, de petite taille, comprenant en moyenne 120 ménages.

Utilisez la barre latérale à gauche pour sélectionner une méthode d'échantillonnage et configurer ses paramètres.
""")
st.markdown("---")

# Load the data
df_frame = load_data()

if df_frame is not None:
    # Display initial data summary if desired (can be behind an expander)
    with st.expander("Afficher les détails du cadre de sondage initial"):
        st.subheader("Aperçu du Cadre de Sondage (Premières lignes)")
        st.dataframe(df_frame.head())

        st.subheader("Informations sur le Cadre de Sondage")
        buffer = StringIO()
        df_frame.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.subheader("Statistiques Descriptives Initiales (Variables Numériques du Cadre)")
        st.dataframe(df_frame.describe())

        st.subheader("Dimensions du Cadre de Sondage")
        st.write(f"Nombre de blocs (lignes) : {df_frame.shape[0]}")
        st.write(f"Nombre de variables (colonnes) : {df_frame.shape[1]}")

    # --- SAMPLING METHOD SELECTION AND LOGIC ---
    st.sidebar.header("Méthode d'Échantillonnage")
    sampling_method = st.sidebar.selectbox(
        "Choisir la méthode:",
        ["--Select--", "SAS (Aléatoire Simple Sans Remise)", "Stratifié (Allocation Proportionnelle)"]
    )

    # ... (Rest of your SAS and Stratified sampling code remains the same as before) ...
    # (I'm not repeating the entire sampling logic here for brevity,
    #  just make sure to paste the parts for SAS and Stratified methods below this point)

    if sampling_method == "SAS (Aléatoire Simple Sans Remise)":
        st.header("Méthode: Aléatoire Simple Sans Remise (SAS)")

        # --- SAS User Inputs ---
        st.sidebar.subheader("Paramètres SAS")
        n_sas = st.sidebar.number_input(
            "Taille de l'échantillon (n):",
            min_value=1,
            max_value=len(df_frame),
            value=min(100, len(df_frame)),
            step=10,
            key="n_sas_input"
        )

        potential_comp_vars = [col for col in df_frame.columns
                               if (df_frame[col].nunique() < 50 or df_frame[col].dtype == 'object') and
                               col not in ['CODE GOUV', 'CODE DELEG', 'CODE SECTOR', 'CODE BLOCK', 'Block', 'Cumulative population']]
        if not potential_comp_vars:
            potential_comp_vars = ['Area']

        comp_var_sas_default_index = potential_comp_vars.index('Area') if 'Area' in potential_comp_vars else 0
        comp_var_sas = st.sidebar.selectbox(
            "Variable comparative échantillon-cadre:",
            potential_comp_vars,
            index=comp_var_sas_default_index,
            key="comp_var_sas_select"
        )

        if st.sidebar.button("Générer l'échantillon SAS", key="sas_button"):
            if n_sas > len(df_frame):
                st.error(f"La taille de l'échantillon ({n_sas}) ne peut pas dépasser la taille de la population ({len(df_frame)}).")
            else:
                sample_sas = df_frame.sample(n=n_sas, replace=False, random_state=42)

                st.subheader("1. Échantillon SAS")
                st.dataframe(sample_sas)
                st.download_button(
                    label="Télécharger l'échantillon SAS (CSV)",
                    data=to_csv(sample_sas),
                    file_name='echantillon_sas.csv',
                    mime='text/csv',
                    key='download_sample_sas'
                )

                st.subheader("2. Statistiques Descriptives (Échantillon SAS)")
                numeric_cols_for_desc_sas = sample_sas.select_dtypes(include=np.number).columns.tolist()
                numeric_cols_for_desc_sas = [col for col in numeric_cols_for_desc_sas if not col.startswith('CODE')]
                if 'Cumulative population' in numeric_cols_for_desc_sas:
                    numeric_cols_for_desc_sas.remove('Cumulative population')

                if numeric_cols_for_desc_sas:
                    desc_stats_sas = sample_sas[numeric_cols_for_desc_sas].describe()
                    st.dataframe(desc_stats_sas)
                    st.download_button(
                        label="Télécharger Statistiques SAS (CSV)",
                        data=to_csv(desc_stats_sas.T.reset_index()), # Transpose and reset for better CSV
                        file_name='statistiques_descriptives_sas.csv',
                        mime='text/csv',
                        key='download_stats_sas'
                    )
                else:
                    st.warning("Aucune colonne numérique appropriée trouvée pour les statistiques descriptives.")


                st.subheader(f"3. Tableau Comparatif: {comp_var_sas}")
                props_sample = sample_sas[comp_var_sas].value_counts(normalize=True).mul(100).round(2).rename("Proportion Échantillon (%)")
                props_frame = df_frame[comp_var_sas].value_counts(normalize=True).mul(100).round(2).rename("Proportion Cadre (%)")

                comparison_df = pd.concat([props_sample, props_frame], axis=1).fillna(0)
                comparison_df.index.name = comp_var_sas
                st.dataframe(comparison_df)
                st.download_button(
                    label=f"Télécharger Tableau Comparatif {comp_var_sas} (CSV)",
                    data=to_csv(comparison_df.reset_index()),
                    file_name=f'comparaison_{comp_var_sas}_sas.csv',
                    mime='text/csv',
                    key='download_comp_table_sas'
                )

                st.subheader(f"4. Graphique Comparatif: {comp_var_sas} ")
                try:
                    N_TOP_CATEGORIES = 20
                    top_categories_in_sample = props_sample.head(N_TOP_CATEGORIES).index.tolist()
                    plot_df = comparison_df.loc[top_categories_in_sample]

                    if not plot_df.empty:
                        fig, ax = plt.subplots(figsize=(12, 7))
                        plot_df.plot(kind='bar', ax=ax)
                        ax.set_ylabel("Pourcentage (%)")
                        ax.set_title(f"Comparaison des proportions pour '{comp_var_sas}' (Top {len(plot_df)} de l'échantillon)")
                        ax.tick_params(axis='x', rotation=70, labelsize=8)
                        plt.tight_layout()
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png", bbox_inches='tight')
                        st.download_button(
                            label="Télécharger le Graphique (PNG)",
                            data=buf.getvalue(),
                            file_name=f"graphique_comparaison_{comp_var_sas}_sas.png",
                            mime="image/png",
                            key='download_graph_sas_top_n'
                        )
                    else:
                        st.warning(f"Aucune donnée à afficher pour le graphique de '{comp_var_sas}' (échantillon possiblement trop petit ou variable sans catégories fréquentes).")
                except Exception as e:
                    st.error(f"Erreur lors de la génération du graphique : {e}")


    elif sampling_method == "Stratifié (Allocation Proportionnelle)":
        st.header("Méthode: Stratification à Allocation Proportionnelle")

        st.sidebar.subheader("Paramètres Stratification")
        n_strat = st.sidebar.number_input(
            "Taille totale de l'échantillon (n):",
            min_value=1,
            max_value=len(df_frame),
            value=min(100, len(df_frame)),
            step=10,
            key="n_strat_input"
        )
        strat_var_options = ["Region", "GOVERNORATE", "DELEGATION"]
        strat_var = st.sidebar.selectbox(
            "Variable de stratification:",
            strat_var_options,
            key="strat_var_select"
        )

        if st.sidebar.button("Générer l'échantillon Stratifié", key="strat_button"):
            if n_strat > len(df_frame):
                st.error(f"La taille de l'échantillon ({n_strat}) ne peut pas dépasser la taille de la population ({len(df_frame)}).")
            else:
                st.subheader("1. Tableau des Allocations (nh) par Strate")

                stratum_pop_counts = df_frame.groupby(strat_var)['pop_block'].sum().rename('Population Strate (N_h)')
                N_total = df_frame['pop_block'].sum()
                stratum_weights = (stratum_pop_counts / N_total) # Renamed later for display with %
                n_h_float = (stratum_weights * n_strat) # Renamed later for display

                n_h_int = np.floor(n_h_float).astype(int)
                remainder_sum_to_distribute = n_strat - n_h_int.sum()

                if remainder_sum_to_distribute > 0:
                    fractional_parts = n_h_float - n_h_int
                    stratum_actual_sizes_for_alloc = df_frame.groupby(strat_var).size()
                    temp_alloc_df = pd.DataFrame({
                        'n_h_int': n_h_int,
                        'fractional': fractional_parts,
                        'actual_size': stratum_actual_sizes_for_alloc
                    }).sort_values(by='fractional', ascending=False)

                    for idx in temp_alloc_df.index:
                        if remainder_sum_to_distribute == 0:
                            break
                        if n_h_int.loc[idx] < temp_alloc_df.loc[idx, 'actual_size']:
                            n_h_int.loc[idx] += 1
                            remainder_sum_to_distribute -= 1

                # Final adjustment if sum still doesn't match (e.g., n_strat too small or strata too restrictive)
                if n_h_int.sum() != n_strat:
                    diff_to_distribute = n_strat - n_h_int.sum()
                    if diff_to_distribute > 0 :
                        eligible_strata_for_remainder_final = n_h_int[n_h_int < df_frame.groupby(strat_var).size()].index.tolist()
                        for _ in range(int(diff_to_distribute)):
                            if not eligible_strata_for_remainder_final: break
                            # Prioritize strata that have non-zero theoretical allocation and can still be incremented
                            potential_strata = n_h_float[eligible_strata_for_remainder_final][n_h_float[eligible_strata_for_remainder_final]>0].sort_values(ascending=False).index
                            incremented_this_round = False
                            for stratum_to_increment in potential_strata:
                                if n_h_int.loc[stratum_to_increment] < df_frame.groupby(strat_var).size().loc[stratum_to_increment]:
                                    n_h_int.loc[stratum_to_increment] += 1
                                    incremented_this_round = True
                                    break # Increment one stratum per pass of the remainder
                            if not incremented_this_round and eligible_strata_for_remainder_final: # Fallback if all eligible have 0 theoretical, pick largest available
                                stratum_to_increment = df_frame.groupby(strat_var).size().loc[eligible_strata_for_remainder_final].idxmax()
                                if n_h_int.loc[stratum_to_increment] < df_frame.groupby(strat_var).size().loc[stratum_to_increment]:
                                     n_h_int.loc[stratum_to_increment] += 1
                            # Update eligibility (this part can be complex to make perfect for all edge cases)
                            eligible_strata_for_remainder_final = n_h_int[n_h_int < df_frame.groupby(strat_var).size()].index.tolist()


                n_h_final = n_h_int.rename('Allocation Ajustée (n_h)')

                # Cap at actual stratum size (safeguard)
                stratum_sizes_df_final_check = df_frame.groupby(strat_var).size()
                for s_val, alloc in n_h_final.items():
                    if alloc > stratum_sizes_df_final_check[s_val]:
                        n_h_final[s_val] = stratum_sizes_df_final_check[s_val]

                n_strat_final_adjusted = n_h_final.sum()
                if n_strat_final_adjusted != n_strat and abs(n_strat_final_adjusted - n_strat) > 0: # Show warning only if different
                     st.warning(f"La taille totale de l'échantillon a été ajustée à {n_strat_final_adjusted} en raison des contraintes de taille des strates et de l'arrondissement.")

                allocation_df = pd.DataFrame({
                    'Population Strate (N_h)': stratum_pop_counts,
                    'Poids Strate (W_h %)': (stratum_weights * 100).round(2),
                    'Allocation Théorique (n*W_h)': n_h_float.round(3),
                    'Allocation Ajustée (n_h)': n_h_final
                })
                st.dataframe(allocation_df)
                st.download_button(
                    label="Télécharger Tableau d'Allocation (CSV)",
                    data=to_csv(allocation_df.reset_index()),
                    file_name='allocations_strat.csv',
                    mime='text/csv',
                    key='download_alloc_table_strat'
                )

                stratified_sample_list = []
                for stratum_value, num_to_sample in n_h_final.items():
                    if num_to_sample > 0:
                        stratum_df = df_frame[df_frame[strat_var] == stratum_value]
                        actual_sample_size_for_stratum = min(int(num_to_sample), len(stratum_df))
                        if actual_sample_size_for_stratum > 0 :
                             stratum_sample = stratum_df.sample(n=actual_sample_size_for_stratum, replace=False, random_state=42)
                             stratified_sample_list.append(stratum_sample)

                if stratified_sample_list:
                    final_stratified_sample = pd.concat(stratified_sample_list)
                    st.subheader("2. Échantillon Stratifié")
                    st.dataframe(final_stratified_sample)
                    st.download_button(
                        label="Télécharger l'échantillon Stratifié (CSV)",
                        data=to_csv(final_stratified_sample),
                        file_name='echantillon_strat.csv',
                        mime='text/csv',
                        key='download_sample_strat'
                    )

                    st.subheader("3. Statistiques Descriptives (Échantillon Stratifié)")
                    numeric_cols_for_strat_desc = final_stratified_sample.select_dtypes(include=np.number).columns.tolist()
                    numeric_cols_for_strat_desc = [col for col in numeric_cols_for_strat_desc if not col.startswith('CODE')]
                    if 'Cumulative population' in numeric_cols_for_strat_desc:
                        numeric_cols_for_strat_desc.remove('Cumulative population')

                    if numeric_cols_for_strat_desc:
                        desc_stats_strat = final_stratified_sample[numeric_cols_for_strat_desc].describe()
                        st.dataframe(desc_stats_strat)
                        st.download_button(
                            label="Télécharger Statistiques Stratifiées (CSV)",
                            data=to_csv(desc_stats_strat.T.reset_index()),
                            file_name='statistiques_descriptives_strat.csv',
                            mime='text/csv',
                            key='download_stats_strat'
                        )
                    else:
                        st.warning("Aucune colonne numérique appropriée trouvée pour les statistiques descriptives dans l'échantillon stratifié.")
                else:
                    st.warning("Aucun échantillon n'a pu être tiré (taille d'échantillon demandée trop petite ou strates vides après allocation).")

    elif sampling_method == "--Select--":
        st.info("Veuillez sélectionner une méthode d'échantillonnage dans la barre latérale.")

else:
    st.warning("Le cadre de sondage n'a pas pu être chargé. Veuillez vérifier le fichier et le chemin d'accès.")
