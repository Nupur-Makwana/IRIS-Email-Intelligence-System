# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:53:48 2026

@author: nupur
"""

import pandas as pd

# Load cleaned Enron emails
input_path = r"E:\IRIS\dataset\clean_emails.csv"

df = pd.read_csv(input_path)

# Combine subject + body
df["text"] = (
    df["subject"].fillna("") + " " +
    df["body"].fillna("")
).str.lower()


# -----------------------------
# HIGH PRIORITY INDICATORS
# -----------------------------

high_keywords = [
    "urgent",
    "urgently",
    "asap",
    "immediately",
    "action required",
    "deadline",
    "due today",
    "due tomorrow",
    "critical",
    "emergency",
    "please respond",
    "please confirm",
    "interview",
    "security alert",
    "account suspended",
    "final notice"
]


# -----------------------------
# LOW PRIORITY INDICATORS
# -----------------------------

low_keywords = [
    "newsletter",
    "unsubscribe",
    "promotion",
    "promotional",
    "sale",
    "discount",
    "special offer",
    "advertisement",
    "weekly newsletter",
    "monthly newsletter",
    "daily digest"
]


def count_keywords(text, keywords):
    return sum(keyword in text for keyword in keywords)


# Count indicators
df["high_score"] = df["text"].apply(
    lambda x: count_keywords(x, high_keywords)
)

df["low_score"] = df["text"].apply(
    lambda x: count_keywords(x, low_keywords)
)


# -----------------------------
# CREATE CANDIDATE LABEL
# -----------------------------

df["priority_candidate"] = "MEDIUM"

# HIGH if high indicators exist
df.loc[df["high_score"] >= 1, "priority_candidate"] = "HIGH"

# LOW if low indicators exist
df.loc[
    (df["low_score"] >= 1) &
    (df["high_score"] == 0),
    "priority_candidate"
] = "LOW"


# -----------------------------
# SHOW RESULTS
# -----------------------------

print("\nCandidate distribution:")
print(df["priority_candidate"].value_counts())

print("\nHIGH examples:")
print(
    df[df["priority_candidate"] == "HIGH"]["subject"]
    .head(20)
    .to_string(index=False)
)

print("\nLOW examples:")
print(
    df[df["priority_candidate"] == "LOW"]["subject"]
    .head(20)
    .to_string(index=False)
)


# Save candidates
output_path = r"E:\IRIS\dataset\priority_candidates.csv"

df.to_csv(output_path, index=False)

print("\nCandidate dataset saved to:")
print(output_path)