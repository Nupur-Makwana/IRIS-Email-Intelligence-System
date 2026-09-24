# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:30:46 2026

@author: nupur
"""

import pandas as pd
from rouge_score import rouge_scorer
import sys

sys.path.append(r"E:\IRIS\src")

from summarization import summarize_email

INPUT_PATH = r"E:\IRIS\dataset\summarization_evaluation.csv"
OUTPUT_PATH = r"E:\IRIS\results\summarization_metrics.csv"

df = pd.read_csv(INPUT_PATH)

scorer = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True
)

results = []

for _, row in df.iterrows():

    generated_summary = summarize_email(
        row["subject"],
        row["body"]
    )

    scores = scorer.score(
        row["reference_summary"],
        generated_summary
    )

    results.append({
        "email_id": row["email_id"],
        "rouge1": scores["rouge1"].fmeasure,
        "rouge2": scores["rouge2"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure
    })

results_df = pd.DataFrame(results)

average_scores = {
    "ROUGE-1": results_df["rouge1"].mean(),
    "ROUGE-2": results_df["rouge2"].mean(),
    "ROUGE-L": results_df["rougeL"].mean()
}

print("\n===== SUMMARIZATION EVALUATION =====")

for metric, score in average_scores.items():
    print(f"{metric}: {score:.4f}")

results_df.to_csv(OUTPUT_PATH, index=False)

print("\nDetailed results saved to:")
print(OUTPUT_PATH)