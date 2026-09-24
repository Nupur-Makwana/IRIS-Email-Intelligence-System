# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 19:00:12 2026

@author: nupur
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

cm = np.array([
    [50, 0, 0],
    [2, 44, 4],
    [0, 3, 47]
])

labels = ["HIGH", "MEDIUM", "LOW"]

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels
)

plt.title("Priority Classification Confusion Matrix")
plt.xlabel("Predicted Priority")
plt.ylabel("Actual Priority")

plt.tight_layout()

plt.savefig(
    r"E:\IRIS\results\priority_confusion_matrix_nb.png",
    dpi=300
)

plt.show()