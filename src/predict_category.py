# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:56:03 2026

@author: nupur
"""

import joblib
import sys

sys.path.append(r"E:\IRIS\src")

from preprocessing import preprocess_text

MODEL_PATH = r"E:\IRIS\models\category_lr_model.pkl"
VECTORIZER_PATH = r"E:\IRIS\models\category_tfidf_vectorizer.pkl"

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)


def predict_category(subject, body):
    text = str(subject) + " " + str(body)
    clean_text = preprocess_text(text)

    text_tfidf = tfidf.transform([clean_text])

    prediction = model.predict(text_tfidf)[0]

    return prediction


if __name__ == "__main__":

    test_emails = [
        (
            "Technical Interview Confirmation",
            "Your technical interview is scheduled for tomorrow at 10 AM. Please confirm your availability and keep your resume ready."
        ),
        (
            "Department Meeting Reminder",
            "This is a reminder that the department meeting will be held on Friday at 2 PM. Please attend the meeting."
        ),
        (
            "Weekend Store Discount",
            "Get 40 percent off on selected products this weekend. Shop now and enjoy our special offer."
        ),
        (
            "Flight Booking Confirmation",
            "Your flight to Mumbai is confirmed for Monday at 8 AM. Please arrive at the airport two hours before departure."
        )
    ]

    for subject, body in test_emails:
        category = predict_category(subject, body)

        print("\nSubject:", subject)
        print("Predicted Category:", category)