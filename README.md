# Projet Steam - Analyse exploratoire du marche des jeux video

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=fff)](#)
[![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=flat&logo=apachespark&logoColor=fff)](#)
[![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=flat&logo=databricks&logoColor=fff)](#)
[![AWS S3](https://img.shields.io/badge/AWS_S3-569A31?style=flat&logo=amazons3&logoColor=fff)](#)
[![JEDHA](https://img.shields.io/badge/JEDHA-blueviolet?style=flat)](#)

---

## About

Ce projet realise une **analyse exploratoire (EDA)** du catalogue de jeux video disponibles sur la plateforme **Steam**.
Il repond a la problematique : quels facteurs influencent la popularite et le succes commercial d'un jeu video ?

Realise dans le cadre du **Bootcamp JEDHA** (Bloc 2 - Analyse exploratoire, visualisation et pre-processing), ce travail analyse environ 55 000 jeux sous trois angles :
- **Macro-analyse** : editeurs dominants, impact du COVID sur les sorties, politique tarifaire, langues supportees, restrictions d'age
- **Genres** : genres populaires, satisfaction joueurs, specialisation des editeurs, rentabilite
- **Plateformes** : repartition Windows/Mac/Linux, correlation genre-plateforme

---

## Dataset

- **Source** : fichier JSON semi-structure heberge sur AWS S3 (Data Lake Jedha)
- **Volume** : ~55 000 jeux avec prix, genre, editeur, developpeur, notes, plateformes, langues et date de sortie
- **Acces** : `s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json`

---

## Installation

Ce notebook est concu pour etre execute sur **Databricks** (cluster PySpark). Aucune installation locale n'est requise.

Pour une execution locale, installer PySpark :

```bash
pip install pyspark
```

---

## Pipeline

| #  | Analyse | Question traitee |
|----|---------|-----------------|
| 1  | Top publishers et developers | Quel editeur a publie le plus de jeux ? |
| 2  | Sorties par annee + focus COVID | Y a-t-il des annees avec plus de sorties ? |
| 3  | Distribution des prix | Comment les prix sont-ils distribues ? |
| 4  | Top langues supportees | Quelles sont les langues les plus representees ? |
| 5  | Restrictions d'age (16+/18+) | Quelle part de jeux est reservee aux adultes ? |
| 6  | Hall of Fame (top 10 jeux) | Quels sont les jeux les mieux notes ? |
| 7  | Genres les plus representes | Quels genres dominent le catalogue ? |
| 8  | Rating moyen par genre | Quels genres obtiennent les meilleurs avis ? |
| 9  | Genres les plus lucratifs | Quels genres ont le prix moyen le plus eleve ? |
| 10 | ADN des editeurs par genre | Les editeurs ont-ils des genres de predilection ? |
| 11 | Distribution Win/Mac/Linux | Les jeux sont-ils disponibles sur tous les OS ? |
| 12 | Support OS par genre | Certains genres privilegient-ils un OS ? |
| 13 | Analyse des promotions | Quelle part du catalogue est en promotion ? |

**Stack technique** :

| Outil | Usage |
|-------|-------|
| **PySpark** | Traitement distribue des donnees (DataFrames, transformations) |
| **Databricks** | Environnement d'execution, visualisation et dashboarding |
| **AWS S3** | Data Lake, stockage de la source JSON |
| **Python** | Langage principal, fonctions natives (`builtins.round`) |

---

## Resultats

- L'effet COVID est significatif : +20% de sorties en 2020, +24% en 2021 par rapport a 2019.
- Windows domine a plus de 95% du catalogue. Mac et Linux restent marginaux mais non negligeables pour certains genres (Indie, Casual).
- L'anglais est la langue incontournable pour une sortie mondiale.
- Les genres Action et Indie dominent en volume, tandis que Simulation et Strategy affichent les prix moyens les plus eleves.
- Seule une faible proportion du catalogue est en promotion a un instant donne.

---

## Conclusion

L'analyse repond a la problematique : **quels facteurs influencent la popularite et le succes commercial d'un jeu video sur Steam ?**

- L'effet COVID est significatif : +20% de sorties en 2020, +24% en 2021 par rapport a 2019.
- Windows domine a plus de 95% du catalogue. Mac et Linux restent marginaux mais non negligeables pour certains genres (Indie, Casual).
- L'anglais est la langue incontournable pour une sortie mondiale.
- Les genres Action et Indie dominent en volume, tandis que Simulation et Strategy affichent les prix moyens les plus eleves.

**Recommandation Ubisoft** : pour maximiser les chances de succes d'un titre AAA, cibler Windows en priorite, supporter l'anglais au minimum, et positionner le prix en coherence avec le genre.

---

## Structure du projet

```
STEAM_BLOC-2_JEDHA_FORMATION/
├── STEAM PROJECT.ipynb    # Notebook PySpark (EDA complete)
├── requirements.txt       # Dependances Python
├── .gitignore
└── README.md
```

---

## Auteur

Athanor SAVOUILLAN · [GitHub](https://github.com/athanormark)
