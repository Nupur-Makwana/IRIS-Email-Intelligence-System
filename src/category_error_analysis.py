# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 21:26:04 2026

@author: nupur
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

file_path = r"E:\IRIS\dataset\category_dataset_processed.csv"

df = pd.read_csv(file_path)

X = df["clean_text"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

model = LogisticRegression(
    max_iter=1000
)

model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

results = df.loc[X_test.index, [
    "email_id",
    "subject",
    "category"
]].copy()

results["predicted_category"] = y_pred

errors = results[
    results["category"] != results["predicted_category"]
]

print("Total test emails:", len(results))
print("Correct predictions:", len(results) - len(errors))
print("Incorrect predictions:", len(errors))

print("\nERROR ANALYSIS:")
print(errors.to_string(index=False))

print("\nCONFUSION BY ACTUAL AND PREDICTED CATEGORY:")
print(
    errors.groupby(
        ["category", "predicted_category"]
    ).size()
)