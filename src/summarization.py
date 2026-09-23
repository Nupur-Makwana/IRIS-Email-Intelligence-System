# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 08:56:25 2026

@author: nupur
"""

import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

def split_sentences(text):
    text = re.sub(r'([.!?])(?=[A-Z])', r'\1 ', text)
    text = re.sub(r',(?=I\s)', ', ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def summarize_email(subject, body, max_sentences=2):
    text = f"{subject}. {body}"
    sentences = split_sentences(text)

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(sentences)
    scores = np.asarray(matrix.sum(axis=1)).ravel()
    ranked_indices = np.argsort(scores)[::-1][:max_sentences]
    selected_indices = sorted(ranked_indices)
    summary = " ".join(
        sentences[i] for i in selected_indices
    )

    return summary


if __name__ == "__main__":
    subject = "Urgent Interview Confirmation"

    body = """
    Hi Nupur,
    I hope you had a good weekend.
    The weather has been quite pleasant lately.
    I wanted to share a few updates regarding our project.
    We have completed the database design and frontend prototype.
    The backend integration is still pending.
    Our project review has been moved to Friday at 2 PM.
    Please prepare the system demonstration and bring the latest presentation.
    The review will be conducted in Lab 3.
    Let me know if you have any questions.
    Regards,
    Project Coordinator
    """

    summary = summarize_email(subject, body)

    print("\nOriginal Email:")
    print(body)

    print("\nGenerated Summary:")
    print(summary)
if __name__ == "__main__":
    test = "Hi Nupur,I hope you had a good weekend.The weather has been quite pleasant lately.I wanted to share a few updates regarding our project.We have completed the database design and frontend prototype.The backend integration is still pending.Our project review has been moved to Friday at 2 PM.Please prepare the system demonstration and bring the latest presentation."

    print(split_sentences(test))