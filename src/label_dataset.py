# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:44:21 2026

@author: nupur
"""

import pandas as pd

# Load cleaned emails
input_path = r"E:\IRIS\dataset\clean_emails.csv"

df = pd.read_csv(input_path)

# Combine subject and body
df["text"] = (
    df["subject"].fillna("") + " " +
    df["body"].fillna("")
).str.lower()


# Priority keywords
high_keywords = [
    "urgent", "urgently", "asap", "immediately",
    "action required", "deadline", "due today",
    "due tomorrow", "critical", "emergency",
    "interview", "security alert", "important action"
]

low_keywords = [
    "newsletter", "unsubscribe", "promotion",
    "promotional", "sale", "discount",
    "advertisement", "weekly update",
    "monthly newsletter"
]


def contains_keyword(text, keywords):
    return any(keyword in text for keyword in keywords)


# Create candidate labels
df["priority_candidate"] = "MEDIUM"

df.loc[
    df["text"].apply(lambda x: contains_keyword(x, high_keywords)),
    "priority_candidate"
] = "HIGH"

df.loc[
    df["text"].apply(lambda x: contains_keyword(x, low_keywords)),
    "priority_candidate"
] = "LOW"


# Show distribution
print("\nCandidate priority distribution:")
print(df["priority_candidate"].value_counts())

print("\nExamples of HIGH:")
print(df[df["priority_candidate"] == "HIGH"]["subject"].head(10).to_string(index=False))

print("\nExamples of LOW:")
print(df[df["priority_candidate"] == "LOW"]["subject"].head(10).to_string(index=False))