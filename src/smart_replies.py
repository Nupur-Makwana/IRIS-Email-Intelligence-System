# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:22:27 2026

@author: nupur
"""

import re


def generate_smart_replies(subject, body):
    """
    Generate lightweight, rule-based smart reply suggestions
    based on the content of an email.
    """

    text = f"{subject} {body}".lower()

    replies = []

    # Interview / job-related emails
    if any(word in text for word in [
        "interview", "job", "internship", "application", "selection"
    ]):
        replies.append(
            "Thank you for the update. I appreciate the opportunity."
        )
        replies.append(
            "Thank you for letting me know. I confirm my availability."
        )
        replies.append(
            "I appreciate the update. I will be prepared as required."
        )

    # Meeting-related emails
    elif any(word in text for word in [
        "meeting", "call", "discussion", "appointment", "schedule"
    ]):
        replies.append(
            "Thank you for the update. I confirm my availability."
        )
        replies.append(
            "Noted. I will attend the meeting as scheduled."
        )
        replies.append(
            "Thanks for letting me know. The scheduled time works for me."
        )

    # Project / work-related emails
    elif any(word in text for word in [
        "project", "task", "deadline", "presentation", "review", "work"
    ]):
        replies.append(
            "Thank you for the update. I will take care of it."
        )
        replies.append(
            "Noted. I will complete the required work on time."
        )
        replies.append(
            "Thanks for the information. I will review the details and proceed accordingly."
        )

    # Request-related emails
    elif any(word in text for word in [
        "request", "please", "need", "required", "submit"
    ]):
        replies.append(
            "Thank you for your message. I will look into this."
        )
        replies.append(
            "Noted. I will provide the required information shortly."
        )
        replies.append(
            "Thank you for letting me know. I will take the necessary action."
        )

    # General fallback
    else:
        replies.append(
            "Thank you for your email. I have received your message."
        )
        replies.append(
            "Thanks for the information. I will review it and get back to you."
        )
        replies.append(
            "Thank you for the update. I will get back to you shortly."
        )

    return replies