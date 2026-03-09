# Databricks notebook source

# MAGIC %md
# MAGIC # 🎮 Analyse Strategique Globale du Marche Steam - Projet Ubisoft
# MAGIC
# MAGIC ## 📝 Contexte et Objectifs
# MAGIC Dans le cadre du developpement de notre nouveau titre AAA, la direction d'Ubisoft souhaite une analyse approfondie de l'ecosysteme Steam actuel. Ce rapport d'analyse exploratoire (EDA) vise a identifier les facteurs cles de succes et les tendances du marche.
# MAGIC
# MAGIC Nous repondrons aux axes d'analyse suivants :
# MAGIC 1.  **Macro-Analyse :** Dynamique temporelle, distribution des prix, langues et restrictions d'age.
# MAGIC 2.  **Performance & Qualite :** Analyse des notes joueurs (Ratings) et des editeurs leaders.
# MAGIC 3.  **Analyse des Genres :** Rentabilite, appreciation critique et specialisation des editeurs.
# MAGIC 4.  **Strategie Technique :** Couverture des plateformes (OS) par genre.
# MAGIC
# MAGIC ## ⚙️ Stack Technique
# MAGIC * **Source :** Data Lake S3 (JSON semi-structure).
# MAGIC * **Moteur :** PySpark (Cluster Databricks).

# COMMAND ----------

# -----------------------------------------------------------------------------
# PHASE 1 : INGESTION ET PREPARATION DES DONNEES (ETL)
# -----------------------------------------------------------------------------

from pyspark.sql.functions import (col, explode, split, try_to_date, year, count,
                                   desc, avg, sum as _sum, when, lit, round, regexp_extract)
import builtins

# 1. Chargement depuis le Data Lake S3
file_path = "s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json"
print("Ingestion des donnees brutes...")
df_raw = spark.read.json(file_path)

# 2. Aplatissement et Selection (Data Cleaning)
df_flat = df_raw.select(
    col("data.name").alias("title"),
    col("data.developer").alias("developer"),
    col("data.publisher").alias("publisher"),
    col("data.genre").alias("genre_string"),
    col("data.initialprice").alias("price_raw"),
    col("data.release_date").alias("date_raw"),
    col("data.required_age").alias("required_age_raw"),
    col("data.languages").alias("languages_string"),
    col("data.positive").alias("positive_reviews"),
    col("data.negative").alias("negative_reviews"),
    col("data.platforms").alias("platforms")
)

# 3. Transformations et Feature Engineering
df_clean = df_flat.withColumn(
    "release_year", year(try_to_date(col("date_raw"), "yyyy/MM/dd"))
).withColumn(
    "price_eur", col("price_raw").cast("double") / 100
).withColumn(
    "required_age", regexp_extract(col("required_age_raw"), r"(\d+)", 1).cast("integer")
).withColumn(
    "required_age", when(col("required_age").isNull(), 0).otherwise(col("required_age"))
).withColumn(
    "total_reviews", col("positive_reviews") + col("negative_reviews")
).withColumn(
    "rating_pct", when(col("total_reviews") > 0,
                       round((col("positive_reviews") / col("total_reviews")) * 100, 2)
                  ).otherwise(0)
)

# 4. Creation de vues specialisees

# A. Vue GENRES
df_genres_exploded = df_clean.select(
    "title", "price_eur", "rating_pct", "total_reviews", "platforms",
    explode(split(col("genre_string"), ", ")).alias("genre")
)

# B. Vue LANGUES
df_languages = df_clean.select(
    "title",
    explode(split(col("languages_string"), ", ")).alias("language")
)

print(f"Pipeline ETL termine. {df_clean.count()} jeux prets.")
display(df_clean.select("title", "required_age", "required_age_raw").limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🌍 Macro-Analyse : Production et Acteurs
# MAGIC
# MAGIC **Questions :**
# MAGIC * Y a-t-il eu un effet "Covid" sur les sorties ?
# MAGIC * Quels sont les editeurs/developpeurs les plus actifs ?

# COMMAND ----------

# --- 1. Dynamique Temporelle ---
df_years = df_clean.filter(col("release_year").isNotNull()) \
                   .groupBy("release_year") \
                   .count() \
                   .orderBy(col("release_year").desc())

print("Sorties par annee :")
display(df_years)

# COMMAND ----------

# --- 2. Top Editeurs (Publishers) ---
df_top_publishers = df_clean.filter(col("publisher").isNotNull()) \
                            .groupBy("publisher") \
                            .count() \
                            .orderBy(desc("count")) \
                            .limit(15)

print("Top 15 Editeurs (Publishers) :")
display(df_top_publishers)

# COMMAND ----------

# --- 3. Top Developpeurs ---
df_top_devs = df_clean.filter(col("developer").isNotNull()) \
                      .groupBy("developer") \
                      .count() \
                      .orderBy(desc("count")) \
                      .limit(10)

print("Top 10 Developpeurs :")
display(df_top_devs)

# COMMAND ----------

# --- 4. Focus COVID : Impact sur les sorties (2018-2022) ---
df_covid = df_clean.filter(col("release_year").between(2018, 2022)) \
                   .groupBy("release_year") \
                   .count() \
                   .orderBy("release_year")

print("Focus COVID - Sorties 2018-2022 :")
display(df_covid)

# Calcul de la variation par rapport a 2019
from pyspark.sql import Row
covid_rows = {row["release_year"]: row["count"] for row in df_covid.collect()}
baseline = covid_rows.get(2019, 1)
for y in [2020, 2021, 2022]:
    if y in covid_rows:
        variation = ((covid_rows[y] - baseline) / baseline) * 100
        print(f"  {y} vs 2019 : {'+' if variation > 0 else ''}{variation:.1f}%")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 💰 Macro-Analyse : Economie et Accessibilite
# MAGIC
# MAGIC **Questions :**
# MAGIC * Quelle est la distribution des prix ?
# MAGIC * Quelles sont les langues indispensables pour une sortie mondiale ?
# MAGIC * Quelle est la part de jeux reserves aux adultes (+16/18) ?

# COMMAND ----------

# --- 5. Distribution des Prix ---
df_prices = df_clean.filter((col("price_eur") > 0) & (col("price_eur") < 100)).select("price_eur")

print("Distribution des prix (Focus marche 1-100 EUR) :")
display(df_prices)

# COMMAND ----------

# --- 6. Analyse des Langues ---
df_top_lang = df_languages.groupBy("language") \
                          .count() \
                          .orderBy(desc("count")) \
                          .limit(10)
print("Top 10 Langues supportees :")
display(df_top_lang)

# COMMAND ----------

# --- 7. Restrictions d'Age (PEGI/ESRB) ---
df_age = df_clean.withColumn(
    "age_category",
    when(col("required_age") >= 18, "18+ (Adults Only)")
    .when(col("required_age") >= 16, "16+ (Mature)")
    .otherwise("General Audience (<16)")
).groupBy("age_category").count()

print("Repartition par categorie d'age :")
display(df_age)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Analyse des Genres : Rentabilite et Qualite
# MAGIC
# MAGIC **Questions :**
# MAGIC * Quels sont les genres les plus lucratifs (Prix moyen) ?
# MAGIC * Quels genres obtiennent les meilleures recommandations des joueurs ?
# MAGIC * Les editeurs ont-ils des genres de predilection ?

# COMMAND ----------

# Agregation complexe par genre : Volume, Prix Moyen, et Satisfaction Client
df_genre_metrics = df_genres_exploded.groupBy("genre") \
    .agg(
        count("title").alias("volume"),
        round(avg("price_eur"), 2).alias("avg_price"),
        round(avg("rating_pct"), 2).alias("avg_rating"),
        round(avg("total_reviews"), 0).alias("avg_engagement")
    ) \
    .filter(col("volume") > 100)

# --- 8. Genres les plus representes (Volume) ---
print("Genres les plus populaires (Volume) :")
display(df_genre_metrics.orderBy(desc("volume")).limit(10))

# COMMAND ----------

# --- 9. Genres les plus lucratifs (Prix Moyen) ---
print("Genres les plus chers (Premium) :")
display(df_genre_metrics.orderBy(desc("avg_price")).limit(10))

# COMMAND ----------

# --- 10. Genres les mieux notes (Qualite Percue) ---
print("Genres avec la meilleure satisfaction moyenne :")
display(df_genre_metrics.orderBy(desc("avg_rating")).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🖥️ Analyse Technique : Plateformes (OS)
# MAGIC
# MAGIC **Questions :**
# MAGIC * La majorite des jeux sont-ils sur Windows, Mac ou Linux ?
# MAGIC * Y a-t-il des genres qui privilegient certaines plateformes ?

# COMMAND ----------

# --- 11. Distribution globale par plateforme ---
total_games = df_clean.count()

df_os_counts = df_clean.select(
    _sum(when(col("platforms.windows") == True, 1).otherwise(0)).alias("Windows"),
    _sum(when(col("platforms.mac") == True, 1).otherwise(0)).alias("Mac"),
    _sum(when(col("platforms.linux") == True, 1).otherwise(0)).alias("Linux"),
    lit(total_games).alias("Total")
)

print("Disponibilite par plateforme :")
display(df_os_counts)

# COMMAND ----------

# Version pivot pour graphique
os_row = df_os_counts.first()
os_data = [
    Row(plateforme="Windows", nb_jeux=os_row["Windows"], pct=builtins.round(os_row["Windows"]/total_games*100, 1)),
    Row(plateforme="Mac", nb_jeux=os_row["Mac"], pct=builtins.round(os_row["Mac"]/total_games*100, 1)),
    Row(plateforme="Linux", nb_jeux=os_row["Linux"], pct=builtins.round(os_row["Linux"]/total_games*100, 1))
]
df_os_pivot = spark.createDataFrame(os_data)

print("Parts de marche par OS :")
display(df_os_pivot)

# COMMAND ----------

# --- 12. Analyse croisee : Support OS par Genre ---
df_platform_genre = df_genres_exploded.select(
    col("genre"),
    when(col("platforms.linux") == True, 1).otherwise(0).alias("is_linux"),
    when(col("platforms.mac") == True, 1).otherwise(0).alias("is_mac")
).groupBy("genre").agg(
    round(avg("is_linux") * 100, 2).alias("linux_support_pct"),
    round(avg("is_mac") * 100, 2).alias("mac_support_pct"),
    count("*").alias("total_games")
).filter(col("total_games") > 500)

print("Support Linux et Mac par Genre :")
display(df_platform_genre.orderBy(desc("linux_support_pct")))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🌟 Analyses Complementaires
# MAGIC
# MAGIC 1.  **Hall of Fame :** Les 10 jeux les mieux notes (minimum de votes significatif).
# MAGIC 2.  **Strategie Promotionnelle :** Analyse du volume de jeux avec remise (Discount).
# MAGIC 3.  **ADN des Editeurs :** Specialisation des Top Publishers par genre.
# MAGIC 4.  **ADN des Studios :** Specialisation des Top Developpeurs par genre.

# COMMAND ----------

# --- 13. Hall of Fame - Top 10 des Meilleurs Jeux ---
df_hall_of_fame = df_clean.filter(col("total_reviews") > 5000) \
                          .select("title", "rating_pct", "total_reviews", "release_year") \
                          .orderBy(desc("rating_pct")) \
                          .limit(10)

print("Hall of Fame - Les 10 jeux les mieux notes :")
display(df_hall_of_fame)

# COMMAND ----------

# --- 14. Analyse des Promotions (Discount) ---
df_discount_raw = df_raw.select(col("data.discount").alias("discount_raw"))

total_with_data = df_discount_raw.filter(col("discount_raw").isNotNull()).count()
discounted = df_discount_raw.filter(
    (col("discount_raw").isNotNull()) &
    (col("discount_raw") != "0") &
    (col("discount_raw") != 0)
).count()

pct_discount = builtins.round(discounted / max(total_with_data, 1) * 100, 1)
print(f"Promotions : {discounted} jeux en promo sur {total_with_data} ({pct_discount}%)")
print(f"   {total_with_data - discounted} jeux au prix normal")

# COMMAND ----------

# --- 15. ADN des Editeurs / Publishers ---
top_pub_names = [row['publisher'] for row in df_top_publishers.limit(5).collect()]

df_pub_dna = df_clean.filter(col("publisher").isin(top_pub_names)) \
                     .select("publisher", explode(split(col("genre_string"), ", ")).alias("genre")) \
                     .groupBy("publisher", "genre") \
                     .count() \
                     .orderBy("publisher", desc("count"))

print("ADN des Editeurs : Genres favoris des Top Publishers :")
display(df_pub_dna)

# COMMAND ----------

# --- 16. ADN des Studios / Developpeurs ---
top_dev_names = [row['developer'] for row in df_top_devs.limit(5).collect()]

df_dev_dna = df_clean.filter(col("developer").isin(top_dev_names)) \
                     .select("developer", explode(split(col("genre_string"), ", ")).alias("genre")) \
                     .groupBy("developer", "genre") \
                     .count() \
                     .orderBy("developer", desc("count"))

print("ADN des Studios : Genres favoris des Top Developpeurs :")
display(df_dev_dna)
