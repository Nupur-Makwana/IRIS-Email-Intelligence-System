# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 17:39:39 2026

@author: nupur
"""

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# -----------------------------------
# 1. Load processed dataset
# -----------------------------------

file_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total emails:", len(df))


# -----------------------------------
# 2. Input and target
# -----------------------------------

X = df["clean_text"]
y = df["priority"]


# -----------------------------------
# 3. Train/Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 4. TF-IDF
# -----------------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


print("\nTF-IDF shape:")
print(X_train_tfidf.shape)


# -----------------------------------
# 5. Train Naive Bayes
# -----------------------------------

print("\nTraining Multinomial Naive Bayes...")

model = MultinomialNB()

model.fit(X_train_tfidf, y_train)

print("Model training completed!")


# -----------------------------------
# 6. Make predictions
# -----------------------------------

y_pred = model.predict(X_test_tfidf)


# -----------------------------------
# 7. Accuracy
# -----------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(f"{accuracy:.4f}")


# -----------------------------------
# 8. Classification Report
# -----------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        labels=["HIGH", "MEDIUM", "LOW"]
    )
)


# -----------------------------------
# 9. Confusion Matrix
# -----------------------------------

print("\nConfusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["HIGH", "MEDIUM", "LOW"]
)

print(cm)