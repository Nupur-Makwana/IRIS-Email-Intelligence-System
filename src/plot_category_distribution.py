# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:22:07 2026

@author: nupur
"""

import pandas as pd
import matplotlib.pyplot as plt

file_path = r"E:\IRIS\dataset\category_dataset_processed.csv"

df = pd.read_csv(file_path)

category_counts = df["category"].value_counts().sort_values(ascending=True)

plt.figure(figsize=(10, 7))

plt.barh(
    category_counts.index,
    category_counts.values
)

plt.title("Category Class Distribution")
plt.xlabel("Number of Emails")
plt.ylabel("Category")

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\category_class_distribution.png",
    dpi=300
)

plt.show()