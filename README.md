# Application de Théorie de Sondage

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sondagewnpc8qgw69uw4s7rhapkb5.streamlit.app/)

**Lien vers l'application déployée :** [https://sondagewnpc8qgw69uw4s7rhapkb5.streamlit.app/](https://sondagewnpc8qgw69uw4s7rhapkb5.streamlit.app/)

## Table des Matières
1.  [Introduction](#introduction)
2.  [Fonctionnalités Principales](#fonctionnalités-principales)
3.  [Base de Sondage](#base-de-sondage)
4.  [Technologies Utilisées](#technologies-utilisées)
5.  [Installation et Lancement Local](#installation-et-lancement-local)
6.  [Comment Utiliser l'Application](#comment-utiliser-lapplication)
7.  [Structure du Projet](#structure-du-projet)

## Introduction

Cette application a été développée dans le cadre d'un projet de Théorie de Sondage. Elle permet aux utilisateurs de tirer automatiquement des échantillons à partir d'un cadre de sondage basé sur les blocs du recensement Tunisien. L'objectif principal est de fournir un outil interactif pour explorer et appliquer deux méthodes d'échantillonnage courantes : l'Échantillonnage Aléatoire Simple Sans Remise (SAS) et l'Échantillonnage Stratifié avec allocation proportionnelle.

## Fonctionnalités Principales ✨

1.  **Chargement de Données :**
    *   L'application charge un cadre de sondage prédéfini (`Cadre Tunisie.csv`).
    *   Affiche un aperçu, des informations générales et des statistiques descriptives du cadre de sondage.

2.  **Deux Méthodes d'Échantillonnage :**
    *   **SAS (Aléatoire Simple Sans Remise) :**
        *   Permet de sélectionner aléatoirement un nombre spécifié d'unités (blocs) du cadre.
        *   Chaque unité a une chance égale d'être choisie.
        *   L'utilisateur peut spécifier la taille de l'échantillon (`n`).
        *   L'utilisateur peut choisir une variable pour comparer la distribution entre l'échantillon et le cadre.
        *   **Sorties :**
            *   Tableau de l'échantillon SAS.
            *   Statistiques descriptives de l'échantillon SAS.
            *   Tableau comparatif des proportions pour la variable choisie (échantillon vs cadre).
            *   Graphique comparatif des proportions.
    *   **Stratifié (Allocation Proportionnelle) :**
        *   Divise la population en sous-groupes (strates) basés sur une variable de stratification choisie par l'utilisateur (Région, Gouvernorat, Délégation).
        *   Tire un échantillon de chaque strate proportionnellement à la taille de cette strate (basée sur `pop_block`) par rapport à la population totale.
        *   L'utilisateur peut spécifier la taille totale de l'échantillon (`n`).
        *   **Sorties :**
            *   Tableau d'allocation indiquant la population, le poids, l'allocation théorique et l'allocation ajustée pour chaque strate.
            *   Tableau de l'échantillon stratifié.
            *   Statistiques descriptives de l'échantillon stratifié.

3.  **Interactivité :**
    *   L'utilisateur peut sélectionner la méthode d'échantillonnage via une barre latérale.
    *   Les paramètres spécifiques à chaque méthode (taille de l'échantillon, variables de stratification/comparaison) sont configurables.

4.  **Téléchargement des Résultats :**
    *   Tous les tableaux générés (échantillons, statistiques, tableaux comparatifs, tableaux d'allocation) peuvent être téléchargés au format CSV.
    *   Les graphiques générés peuvent être téléchargés au format PNG.

## Base de Sondage 📊

L'application utilise un cadre d'échantillonnage nommé `Cadre Tunisie.csv`. Ce cadre est basé sur la division du territoire Tunisien en blocs, conçus à partir du dernier recensement général de la population. Chaque bloc représente une unité géographique relativement homogène, de petite taille, comprenant en moyenne 120 ménages.

**Note Importante :** Pour que l'application fonctionne localement, le fichier `Cadre Tunisie.csv` doit être présent et le chemin d'accès spécifié dans la fonction `load_data` au sein de `app.py` doit être correct. Par défaut, le code pointe vers `C:\Users\dabbe\OneDrive\Desktop\app sondage\Cadre Tunisie.csv`. Vous devrez peut-être ajuster ce chemin ou placer le fichier dans le même répertoire que `app.py` et utiliser un chemin relatif (e.g., `load_data(file_path="Cadre Tunisie.csv")`).

## Technologies Utilisées 🛠️

*   **Python 3.x**
*   **Streamlit:** Pour la création de l'interface web interactive.
*   **Pandas:** Pour la manipulation et l'analyse des données.
*   **NumPy:** Pour les opérations numériques, notamment dans l'allocation stratifiée.
*   **Matplotlib & Seaborn:** Pour la génération des graphiques.

## Installation et Lancement Local 🚀

Pour exécuter cette application sur votre machine locale :

1.  **Clonez le dépôt :**
    ```bash
    git clone <URL_DU_DEPOT_GITHUB>
    cd <NOM_DU_DOSSIER_DU_PROJET>
    ```

2.  **Créez un environnement virtuel (recommandé) :**
    ```bash
    python -m venv venv
    # Sur Windows
    venv\Scripts\activate
    # Sur macOS/Linux
    source venv/bin/activate
    ```

3.  **Installez les dépendances :**
    Assurez-vous que le fichier `requirements.txt` (fourni dans le dépôt) est présent dans le répertoire racine du projet.
    Puis installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
    *Note : Ce fichier `requirements.txt` contient une liste complète des paquets de l'environnement de développement. Pour exécuter cette application spécifique, seules quelques dépendances clés (comme `streamlit`, `pandas`, `numpy`, `matplotlib`, `seaborn`) sont strictement nécessaires, mais l'utilisation du fichier fourni garantit la compatibilité.*

4.  **Placez le fichier de données :**
    Assurez-vous que le fichier `Cadre Tunisie.csv` est accessible par l'application. Soit vous le placez à l'emplacement spécifié dans `app.py` (`C:\Users\dabbe\OneDrive\Desktop\app sondage\Cadre Tunisie.csv`), soit vous modifiez la fonction `load_data` dans `app.py` pour pointer vers le bon chemin (par exemple, si vous placez `Cadre Tunisie.csv` dans le même dossier que `app.py`, changez en `load_data(file_path="Cadre Tunisie.csv")`).

5.  **Lancez l'application Streamlit :**
    ```bash
    streamlit run app.py
    ```
    L'application devrait s'ouvrir automatiquement dans votre navigateur web.

## Comment Utiliser l'Application 📖

1.  **Page d'Accueil :** Une introduction et une description des fonctionnalités sont présentées. Vous pouvez également consulter un aperçu du cadre de sondage initial.
2.  **Sélection de la Méthode :** Utilisez la barre latérale (menu déroulant "Choisir la méthode:") pour sélectionner soit "SAS (Aléatoire Simple Sans Remise)" soit "Stratifié (Allocation Proportionnelle)".
3.  **Configuration des Paramètres :**
    *   **Pour SAS :**
        *   Spécifiez la "Taille de l'échantillon (n)".
        *   Choisissez la "Variable comparative échantillon-cadre".
        *   Cliquez sur "Générer l'échantillon SAS".
    *   **Pour Stratifié :**
        *   Spécifiez la "Taille totale de l'échantillon (n)".
        *   Choisissez la "Variable de stratification".
        *   Cliquez sur "Générer l'échantillon Stratifié".
4.  **Visualisation et Téléchargement des Résultats :**
    *   Les échantillons, statistiques, et autres tableaux/graphiques pertinents seront affichés dans la zone principale.
    *   Utilisez les boutons "Télécharger..." pour sauvegarder les résultats.

## Structure du Projet 📂
.
├── app.py # Le script principal de l'application Streamlit
├── Cadre Tunisie.csv # Le fichier de données du cadre de sondage (doit être présent)
├── requirements.txt # Les dépendances Python du projet
└── README.md # Ce fichier d'information (ce document
