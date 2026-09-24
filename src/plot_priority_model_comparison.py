# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:58:28 2026

@author: nupur
"""
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


file_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df = pd.read_csv(file_path)

X = df["clean_text"]
y = df["priority"]


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


labels = ["HIGH", "MEDIUM", "LOW"]

nb_f1 = f1_score(
    y_test,
    nb_predictions,
    labels=labels,
    average=None
)

lr_f1 = f1_score(
    y_test,
    lr_predictions,
    labels=labels,
    average=None
)


results = pd.DataFrame({
    "Priority": labels,
    "Naive Bayes": nb_f1,
    "Logistic Regression": lr_f1
})


print("\nClass-wise F1 Scores:")
print(results)


x = range(len(labels))
width = 0.35

plt.figure(figsize=(8, 5))

plt.bar(
    [i - width / 2 for i in x],
    results["Naive Bayes"],
    width,
    label="Naive Bayes"
)

plt.bar(
    [i + width / 2 for i in x],
    results["Logistic Regression"],
    width,
    label="Logistic Regression"
)

plt.xticks(x, labels)

plt.xlabel("Priority Class")
plt.ylabel("F1 Score")
plt.title("Priority Classification: Class-wise Model Comparison")

plt.ylim(0, 1.0)

plt.legend()

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\priority_model_comparison.png",
    dpi=300
)

plt.show()