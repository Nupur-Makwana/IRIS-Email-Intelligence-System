# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:30:46 2026

@author: nupur
"""


# -*- coding: utf-8 -*-
"""
IRIS - Summarization Evaluation
Evaluates generated summaries against human-written references.
"""

import pandas as pd
import sys
from pathlib import Path
from rouge_score import rouge_scorer

sys.path.append(r"E:\IRIS\src")

from summarization import summarize_email


# File paths
INPUT_PATH = r"E:\IRIS\dataset\summarization_evaluation.csv"
OUTPUT_PATH = r"E:\IRIS\results\summarization_metrics.csv"

# Load evaluation dataset
df = pd.read_csv(INPUT_PATH)

# Check required columns
required_columns = [
    "email_id",
    "subject",
    "body",
    "reference_summary"
]

missing = [
    column for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Initialize ROUGE evaluator
scorer = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=True
)

results = []

# Evaluate each email
for _, row in df.iterrows():

    generated_summary = summarize_email(
        row["subject"],
        row["body"]
    )

    reference_summary = str(row["reference_summary"])

    scores = scorer.score(
        reference_summary,
        generated_summary
    )

    results.append({
        "email_id": row["email_id"],
        "subject": row["subject"],
        "generated_summary": generated_summary,
        "reference_summary": reference_summary,
        "rouge1": scores["rouge1"].fmeasure,
        "rouge2": scores["rouge2"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure
    })

    # Print individual summaries for quick inspection
    print(f"\n{'=' * 60}")
    print(f"Email ID: {row['email_id']}")
    print(f"Generated: {generated_summary}")
    print(f"Reference: {reference_summary}")
    print(f"ROUGE-1: {scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2: {scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L: {scores['rougeL'].fmeasure:.4f}")

# Save detailed results
results_df = pd.DataFrame(results)

Path(OUTPUT_PATH).parent.mkdir(
    parents=True,
    exist_ok=True
)

results_df.to_csv(OUTPUT_PATH, index=False)

# Calculate average metrics
print("\n===== IRIS SUMMARIZATION EVALUATION =====")
print(f"Emails evaluated: {len(results_df)}")
print(f"ROUGE-1: {results_df['rouge1'].mean():.4f}")
print(f"ROUGE-2: {results_df['rouge2'].mean():.4f}")
print(f"ROUGE-L: {results_df['rougeL'].mean():.4f}")

print("\nDetailed results saved to:")
print(OUTPUT_PATH)



