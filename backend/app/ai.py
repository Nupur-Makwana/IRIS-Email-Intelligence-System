# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:10:44 2026

@author: nupur
"""

import joblib
import sys

sys.path.append(r"E:\IRIS\src")

from preprocessing import preprocess_text
from summarization import summarize_email


MODEL_PATH = r"E:\IRIS\models\priority_nb_model.pkl"
VECTORIZER_PATH = r"E:\IRIS\models\priority_tfidf_vectorizer.pkl"


model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)


def predict_priority(subject, body):
    text = str(subject) + " " + str(body)

    clean_text = preprocess_text(text)

    text_tfidf = tfidf.transform([clean_text])

    prediction = model.predict(text_tfidf)[0]

    return prediction


def generate_summary(subject, body):
    return summarize_email(subject, body)