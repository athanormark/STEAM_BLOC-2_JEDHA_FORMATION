# Projet Steam - Analyse exploratoire du marché des jeux vidéo

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=fff)](#)
[![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=flat&logo=apachespark&logoColor=fff)](#)
[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=fff)](#)
[![AWS S3](https://img.shields.io/badge/AWS_S3-569A31?style=flat&logo=amazons3&logoColor=fff)](#)
[![JEDHA](https://img.shields.io/badge/JEDHA-blueviolet?style=flat)](#)

---

## About

Ce projet réalise une **analyse exploratoire (EDA)** du catalogue de jeux vidéo disponibles sur la plateforme **Steam**.
Il répond à la problématique : quels facteurs influencent la popularité et le succès commercial d'un jeu vidéo ?

Réalisé dans le cadre du **Bootcamp JEDHA** (Bloc 2 - Analyse exploratoire, visualisation et pré-processing), ce travail analyse environ 55 000 jeux sous trois angles :
- **Macro-analyse** : éditeurs dominants, impact du COVID sur les sorties, politique tarifaire, langues supportées, restrictions d'âge
- **Genres** : genres populaires, satisfaction joueurs, spécialisation des éditeurs, rentabilité
- **Plateformes** : répartition Windows/Mac/Linux, corrélation genre-plateforme

---

## Dataset

- **Source** : fichier JSON semi-structuré hébergé sur AWS S3 (Data Lake Jedha)
- **Volume** : ~55 000 jeux avec prix, genre, éditeur, développeur, notes, plateformes, langues et date de sortie
- **Accès** : `s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json`

---

## Installation

Ce notebook est conçu pour être exécuté sur **Databricks** (cluster PySpark). Aucune installation locale n'est requise.

Pour une exécution locale, installer PySpark :

```bash
pip install pyspark
```

---

## Pipeline

| #  | Analyse | Question traitée |
|----|---------|-----------------|
| 1  | Top publishers et developers | Quel éditeur a publié le plus de jeux ? |
| 2  | Sorties par année + focus COVID | Y a-t-il des années avec plus de sorties ? |
| 3  | Distribution des prix | Comment les prix sont-ils distribués ? |
| 4  | Top langues supportées | Quelles sont les langues les plus représentées ? |
| 5  | Restrictions d'âge (16+/18+) | Quelle part de jeux est réservée aux adultes ? |
| 6  | Hall of Fame (top 10 jeux) | Quels sont les jeux les mieux notés ? |
| 7  | Genres les plus représentés | Quels genres dominent le catalogue ? |
| 8  | Rating moyen par genre | Quels genres obtiennent les meilleurs avis ? |
| 9  | Genres les plus lucratifs | Quels genres ont le prix moyen le plus élevé ? |
| 10 | ADN des éditeurs par genre | Les éditeurs ont-ils des genres de prédilection ? |
| 11 | Distribution Win/Mac/Linux | Les jeux sont-ils disponibles sur tous les OS ? |
| 12 | Support OS par genre | Certains genres privilégient-ils un OS ? |
| 13 | Analyse des promotions | Quelle part du catalogue est en promotion ? |

**Stack technique** :

| Outil | Usage |
|-------|-------|
| **PySpark** | Traitement distribué des données (DataFrames, transformations) |
| **Databricks** | Environnement d'exécution, visualisation et dashboarding |
| **AWS S3** | Data Lake, stockage de la source JSON |
| **Python** | Langage principal, fonctions natives (`builtins.round`) |

---

## Résultats

- L'effet COVID est significatif : +20% de sorties en 2020, +24% en 2021 par rapport à 2019.
- Windows domine à plus de 95% du catalogue. Mac et Linux restent marginaux mais non négligeables pour certains genres (Indie, Casual).
- L'anglais est la langue incontournable pour une sortie mondiale.
- Les genres Action et Indie dominent en volume, tandis que Simulation et Strategy affichent les prix moyens les plus élevés.
- Seule une faible proportion du catalogue est en promotion à un instant donné.

---

## Limites

- **Données statiques** : le dataset correspond à un instantané du catalogue Steam à une date donnée. Les tendances identifiées (effet COVID, promotions) ne reflètent pas nécessairement la dynamique actuelle du marché.
- **Absence de données de ventes** : aucune variable de revenus ou de nombre de copies vendues n'est disponible. Les analyses de rentabilité reposent uniquement sur le prix affiché, sans volume de ventes réel.
- **Pas de données temps réel** : le nombre de joueurs connectés, les avis récents ou les mises à jour de contenu ne sont pas couverts par ce dataset.
- **Biais de survie** : le catalogue ne contient que les jeux encore référencés sur Steam. Les titres retirés de la vente (delisted) sont absents, ce qui peut fausser les statistiques sur les genres ou éditeurs historiques.
- **Granularité tarifaire limitée** : les prix promotionnels ne sont captés qu'à l'instant de l'extraction. L'historique des réductions et la fréquence des soldes ne sont pas disponibles.

---

## Conclusion

L'analyse répond à la problématique : **quels facteurs influencent la popularité et le succès commercial d'un jeu vidéo sur Steam ?**

Trois leviers principaux ressortent : le **timing de sortie** (l'effet COVID a montré qu'un contexte favorable peut amplifier les volumes), la **compatibilité plateforme** (Windows reste indispensable, mais le support Mac/Linux élargit l'audience sur les genres Indie et Casual), et le **positionnement tarifaire par genre** (Simulation et Strategy supportent des prix plus élevés que Action ou Indie).

**Recommandations pour Ubisoft** :

1. **Cibler Windows en priorité absolue**, tout en évaluant le portage Mac/Linux pour les titres à dominante Indie ou Casual où la demande multi-plateforme est plus marquée.
2. **Supporter l'anglais au minimum**, et ajouter le chinois simplifié, le russe et le portugais brésilien pour couvrir les marchés à forte croissance identifiés dans le top des langues.
3. **Adapter la stratégie tarifaire au genre** : positionner les titres Simulation et Strategy sur une gamme de prix premium, et les titres Action ou Aventure sur des prix compétitifs alignés avec la densité de l'offre concurrente.
4. **Exploiter les périodes de forte activité** pour planifier les sorties majeures, en s'appuyant sur l'analyse des volumes de publication par année et par trimestre.

---

## Structure du projet

```
STEAM_BLOC-2_JEDHA_FORMATION/
├── STEAM PROJECT.ipynb    # Notebook PySpark (EDA complète)
├── requirements.txt       # Dépendances Python
├── .gitignore
└── README.md
```

---

## Auteur

Athanor SAVOUILLAN · [GitHub](https://github.com/athanormark)
