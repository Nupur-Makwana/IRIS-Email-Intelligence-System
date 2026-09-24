# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:46:26 2026

@author: nupur
"""

import pandas as pd
import matplotlib.pyplot as plt

data_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df = pd.read_csv(data_path)

priority_counts = df["priority"].value_counts()

plt.figure(figsize=(7, 5))

plt.bar(
    priority_counts.index,
    priority_counts.values
)

plt.title("Priority Class Distribution")
plt.xlabel("Priority")
plt.ylabel("Number of Emails")

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\priority_class_distribution.png",
    dpi=300
)

plt.show()