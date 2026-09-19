# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 18:13:20 2026

@author: nupur
"""

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# -----------------------------
# 1. Load processed dataset
# -----------------------------

file_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df = pd.read_csv(file_path)

X = df["clean_text"]
y = df["priority"]


# -----------------------------
# 2. Train-test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------
# 3. Create TF-IDF
# -----------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)

X_train_tfidf = tfidf.fit_transform(X_train)


# -----------------------------
# 4. Train Naive Bayes
# -----------------------------

model = MultinomialNB()

model.fit(X_train_tfidf, y_train)


# -----------------------------
# 5. Save model
# -----------------------------

model_path = r"E:\IRIS\models\priority_nb_model.pkl"
vectorizer_path = r"E:\IRIS\models\priority_tfidf_vectorizer.pkl"

joblib.dump(model, model_path)
joblib.dump(tfidf, vectorizer_path)


print("Priority model saved successfully!")
print("\nModel:")
print(model_path)

print("\nTF-IDF vectorizer:")
print(vectorizer_path)