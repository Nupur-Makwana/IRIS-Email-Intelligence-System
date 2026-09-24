# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:30:32 2026

@author: nupur
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = r"E:\IRIS\results\summarization_metrics.csv"

df = pd.read_csv(file_path)

rouge_scores = {
    "ROUGE-1": df["rouge1"].mean(),
    "ROUGE-2": df["rouge2"].mean(),
    "ROUGE-L": df["rougeL"].mean()
}

print("\nAverage ROUGE Scores:")

for metric, score in rouge_scores.items():
    print(f"{metric}: {score:.4f}")


metrics = list(rouge_scores.keys())
scores = list(rouge_scores.values())

plt.figure(figsize=(7, 5))

plt.bar(
    metrics,
    scores
)

plt.title("Email Summarization ROUGE Scores")
plt.xlabel("ROUGE Metric")
plt.ylabel("F1 Score")

plt.ylim(0, 1.0)

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\summarization_rouge_scores.png",
    dpi=300
)

plt.show()