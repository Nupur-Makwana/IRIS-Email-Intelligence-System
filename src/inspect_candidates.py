# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 09:57:32 2026

@author: nupur
"""

import pandas as pd

input_path = r"E:\IRIS\dataset\priority_candidates.csv"

df = pd.read_csv(input_path)

# Select 30 examples from each category
high = df[df["priority_candidate"] == "HIGH"].head(30)
medium = df[df["priority_candidate"] == "MEDIUM"].head(30)
low = df[df["priority_candidate"] == "LOW"].head(30)

# Keep only useful columns
columns = [
    "email_id",
    "subject",
    "body",
    "high_score",
    "low_score",
    "priority_candidate"
]

high[columns].to_csv(
    r"E:\IRIS\dataset\review_high.csv",
    index=False
)

medium[columns].to_csv(
    r"E:\IRIS\dataset\review_medium.csv",
    index=False
)

low[columns].to_csv(
    r"E:\IRIS\dataset\review_low.csv",
    index=False
)

print("Created review files:")
print("review_high.csv")
print("review_medium.csv")
print("review_low.csv")