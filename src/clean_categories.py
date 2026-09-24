# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 17:46:36 2026

@author: nupur
"""

import pandas as pd

input_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"
output_path = r"E:\IRIS\dataset\category_dataset_processed.csv"

df = pd.read_csv(input_path)

category_mapping = {
    "Event/Workshop": "Event",
    "Event": "Event",
    "Service/Other": "Service",
    "Service": "Service"
}

df["category"] = df["category"].replace(category_mapping)

df.to_csv(output_path, index=False)

print("Category cleanup completed.")
print("\nCategory distribution:")
print(df["category"].value_counts())
print("\nTotal categories:", df["category"].nunique())