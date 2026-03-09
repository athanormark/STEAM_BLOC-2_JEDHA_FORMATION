# 🎮 Projet Steam - Analyse du Marche des Jeux Video

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-3.x-E25A1C?logo=apachespark&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-EDA-FF3621?logo=databricks&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-Data_Source-569A31?logo=amazons3&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📋 Vue d'ensemble

Ce projet est une **Analyse Exploratoire (EDA)** du catalogue de jeux video disponibles sur la plateforme **Steam**, realisee avec **PySpark** sur **Databricks**.

Il repond a la question : *"Quels facteurs influencent la popularite ou les ventes d'un jeu video ?"*

Realise pour le compte d'**Ubisoft**, ce projet analyse le marche (~55 000 jeux) sous 3 axes :
1. **Macro** : editeurs dominants, impact COVID, politique tarifaire, langues, restrictions d'age
2. **Genres** : genres populaires, satisfaction joueurs, specialisation des editeurs, rentabilite
3. **Plateformes** : repartition Windows/Mac/Linux, correlation genre-plateforme

## 🏗️ Architecture Technique

> **Pipeline** : AWS S3 (JSON semi-structure) ➔ Databricks / PySpark ➔ `display()` (Visualisations Databricks)

- **Source** : Dataset JSON depuis le Data Lake S3 Jedha (`steam_game_output.json`)
- **Traitement** : PySpark — schema-on-read, `explode()`, `split()`, `regexp_extract()`
- **Visualisation** : Outil de dashboarding natif Databricks

## 📓 Notebook & Dashboard

| Livrable | Description | Lien |
|----------|-------------|------|
| `STEAM_PROJECT.py` | Notebook PySpark — EDA complete (ETL + Macro + Genres + Plateformes) | [Voir le notebook publie]() |

> **Dashboard** : Le dashboard interactif Databricks sera presente en direct au jury lors de la soutenance.

## 📊 Analyses realisees

| # | Analyse | Question de l'enonce |
|---|---------|---------------------|
| 1 | Top Publishers & Developers | Which publisher has released the most games? |
| 2 | Sorties par annee + Focus COVID | Are there years with more releases? |
| 3 | Distribution des prix | How are the prices distributed? |
| 4 | Top langues supportees | What are the most represented languages? |
| 5 | Restrictions d'age (16+/18+) | Are there many games prohibited for children? |
| 6 | Hall of Fame (Top 10 jeux) | What are the best rated games? |
| 7 | Genres les plus representes | What are the most represented genres? |
| 8 | Rating moyen par genre | Better positive/negative review ratio? |
| 9 | Genres les plus lucratifs | What are the most lucrative genres? |
| 10 | ADN des editeurs par genre | Do some publishers have favorite genres? |
| 11 | Distribution Win/Mac/Linux | Are most games available on Windows/Mac/Linux? |
| 12 | Support OS par genre | Do certain genres tend to be on certain platforms? |
| 13 | Analyse des promotions | Are there many games with a discount? |

## 🛠️ Stack Technique

| Outil | Usage |
|-------|-------|
| **PySpark** | Traitement distribue des donnees (DataFrames, transformations) |
| **Databricks** | Environnement d'execution, visualisation et dashboarding |
| **AWS S3** | Data Lake — stockage de la source JSON |
| **Fonctions cles** | `explode()`, `split()`, `regexp_extract()`, `when()`, `try_to_date()` |

## 📂 Structure du Projet

```
STEAM-_-BLOC-2_JEDHA_FORMATION/
├── STEAM_PROJECT.py   # Notebook Databricks (format natif PySpark)
├── .gitignore
└── README.md
```

## 👤 Auteur
Athanor SAVOUILLAN
