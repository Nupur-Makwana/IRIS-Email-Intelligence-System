# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:28:49 2026

@author: nupur
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


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


nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

nb_predictions = nb_model.predict(X_test_tfidf)


lr_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

lr_model.fit(X_train_tfidf, y_train)

lr_predictions = lr_model.predict(X_test_tfidf)


categories = sorted(y.unique())


nb_f1 = f1_score(
    y_test,
    nb_predictions,
    labels=categories,
    average=None,
    zero_division=0
)

lr_f1 = f1_score(
    y_test,
    lr_predictions,
    labels=categories,
    average=None,
    zero_division=0
)


results = pd.DataFrame({
    "Category": categories,
    "Naive Bayes": nb_f1,
    "Logistic Regression": lr_f1
})


print("\nClass-wise F1 Scores:")
print(results)


results = results.sort_values(
    "Logistic Regression",
    ascending=True
)


y_pos = range(len(results))
height = 0.35

plt.figure(figsize=(11, 9))

plt.barh(
    [i - height / 2 for i in y_pos],
    results["Naive Bayes"],
    height,
    label="Naive Bayes"
)

plt.barh(
    [i + height / 2 for i in y_pos],
    results["Logistic Regression"],
    height,
    label="Logistic Regression"
)

plt.yticks(
    y_pos,
    results["Category"]
)

plt.xlabel("F1 Score")
plt.ylabel("Category")
plt.title("Category Classification: Class-wise Model Comparison")

plt.xlim(0, 1.0)

plt.legend()

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\category_model_comparison.png",
    dpi=300
)

plt.show()