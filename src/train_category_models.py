# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:49:36 2026

@author: nupur
"""

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_PATH = r"E:\IRIS\dataset\category_dataset_processed.csv"
MODEL_PATH = r"E:\IRIS\models\category_lr_model.pkl"
VECTORIZER_PATH = r"E:\IRIS\models\category_tfidf_vectorizer.pkl"

df = pd.read_csv(DATA_PATH)

X = df["clean_text"].fillna("")
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print("TF-IDF features:", X_train_tfidf.shape[1])

nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

nb_predictions = nb_model.predict(X_test_tfidf)

nb_accuracy = accuracy_score(y_test, nb_predictions)

print("\n===== NAIVE BAYES =====")
print("Accuracy:", round(nb_accuracy, 4))
print("\nClassification Report:")
print(classification_report(y_test, nb_predictions, zero_division=0))

print("Confusion Matrix:")
print(confusion_matrix(y_test, nb_predictions))

lr_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

lr_model.fit(X_train_tfidf, y_train)

lr_predictions = lr_model.predict(X_test_tfidf)

lr_accuracy = accuracy_score(y_test, lr_predictions)

print("\n===== LOGISTIC REGRESSION =====")
print("Accuracy:", round(lr_accuracy, 4))
print("\nClassification Report:")
print(classification_report(y_test, lr_predictions, zero_division=0))

print("Confusion Matrix:")
print(confusion_matrix(y_test, lr_predictions))

joblib.dump(lr_model, MODEL_PATH)
joblib.dump(tfidf, VECTORIZER_PATH)

print("\nLogistic Regression category model saved.")
print("TF-IDF vectorizer saved.")