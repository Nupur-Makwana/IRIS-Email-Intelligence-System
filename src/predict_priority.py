# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 09:55:02 2026

@author: nupur
"""
import joblib
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocessing import preprocess_text


# -----------------------------
# Load saved model and vectorizer
# -----------------------------

model_path = r"E:\IRIS\models\priority_nb_model.pkl"
vectorizer_path = r"E:\IRIS\models\priority_tfidf_vectorizer.pkl"

model = joblib.load(model_path)
tfidf = joblib.load(vectorizer_path)

print("Model and TF-IDF vectorizer loaded successfully!")


# -----------------------------
# Function to predict priority
# -----------------------------

def predict_priority(subject, body):

    # Combine subject and body
    text = str(subject) + " " + str(body)

    # Apply the same preprocessing used during training
    clean_text = preprocess_text(text)

    # Convert text into TF-IDF features
    text_tfidf = tfidf.transform([clean_text])

    # Predict priority
    prediction = model.predict(text_tfidf)[0]

    return prediction
# -----------------------------
# Test multiple new emails
# -----------------------------

test_emails = [

    {
        "subject": "Interview Confirmation",
        "body": """
        Dear Nupur,

        Your technical interview has been scheduled for Monday at 10 AM.
        Please confirm your availability as soon as possible.

        Regards,
        HR Team
        """
    },

    {
        "subject": "Department Meeting Reminder",
        "body": """
        Hi Nupur,

        This is a reminder that the department meeting is scheduled
        for next Wednesday at 2 PM. Please attend if you are available.

        Regards,
        Department Office
        """
    },

    {
        "subject": "Weekend Store Discount",
        "body": """
        Hello Nupur,

        Enjoy our weekend sale with discounts of up to 30 percent.
        Browse our latest collection and shop whenever convenient.

        Regards,
        Marketing Team
        """
    }
]


for email in test_emails:

    priority = predict_priority(
        email["subject"],
        email["body"]
    )

    print("\n" + "=" * 60)
    print("Subject:", email["subject"])
    print("Predicted Priority:", priority)