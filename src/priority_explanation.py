# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:25:37 2026

@author: nupur
"""

def explain_priority(subject, body, priority):
    text = f"{subject} {body}".lower()

    high_keywords = [
        "urgent",
        "immediately",
        "emergency",
        "deadline",
        "interview",
        "security",
        "payment",
        "confirmation",
        "today",
        "tomorrow"
    ]

    medium_keywords = [
        "meeting",
        "reminder",
        "update",
        "review",
        "request",
        "schedule",
        "project"
    ]

    matched_high = [
        word for word in high_keywords
        if word in text
    ]

    matched_medium = [
        word for word in medium_keywords
        if word in text
    ]

    if priority == "HIGH":
        if matched_high:
            return (
                "This email was marked HIGH because it contains "
                "important or time-sensitive information such as: "
                + ", ".join(matched_high) + "."
            )

        return (
            "This email was marked HIGH based on the priority "
            "classification model."
        )

    elif priority == "MEDIUM":
        if matched_medium:
            return (
                "This email was marked MEDIUM because it contains "
                "information related to: "
                + ", ".join(matched_medium) + "."
            )

        return (
            "This email was marked MEDIUM based on the priority "
            "classification model."
        )

    else:
        return (
            "This email was marked LOW because the classification "
            "model identified it as less urgent."
        )