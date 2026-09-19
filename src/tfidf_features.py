# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 11:27:18 2026

@author: nupur
"""

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


# -----------------------------------
# 1. Load processed dataset
# -----------------------------------

file_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total emails:", len(df))


# -----------------------------------
# 2. Check priority distribution
# -----------------------------------

print("\nPriority distribution:")
print(df["priority"].value_counts())


# -----------------------------------
# 3. Select input and target
# -----------------------------------

X = df["clean_text"]
y = df["priority"]


# -----------------------------------
# 4. Split dataset
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining emails:", len(X_train))
print("Testing emails:", len(X_test))


# -----------------------------------
# 5. Create TF-IDF Vectorizer
# -----------------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)


# -----------------------------------
# 6. Fit TF-IDF on training data
# -----------------------------------

X_train_tfidf = tfidf.fit_transform(X_train)


# -----------------------------------
# 7. Transform test data
# -----------------------------------

X_test_tfidf = tfidf.transform(X_test)


# -----------------------------------
# 8. Display results
# -----------------------------------

print("\nTF-IDF completed successfully!")

print("\nTraining TF-IDF shape:")
print(X_train_tfidf.shape)

print("\nTesting TF-IDF shape:")
print(X_test_tfidf.shape)

print("\nNumber of vocabulary words/features:")
print(len(tfidf.vocabulary_))


# -----------------------------------
# 9. Display some vocabulary
# -----------------------------------

print("\nFirst 30 TF-IDF features:")

features = tfidf.get_feature_names_out()

for word in features[:30]:
    print(word)