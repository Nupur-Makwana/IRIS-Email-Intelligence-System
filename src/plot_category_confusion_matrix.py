# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:29:38 2026

@author: nupur
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


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
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)


categories = sorted(y.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=categories
)

print("\nCategory Confusion Matrix:")
print(cm)


plt.figure(figsize=(13, 11))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=categories,
    yticklabels=categories
)

plt.title("Category Classification Confusion Matrix")
plt.xlabel("Predicted Category")
plt.ylabel("Actual Category")

plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\category_confusion_matrix_lr.png",
    dpi=300
)

plt.show()