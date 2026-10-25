
# -*- coding: utf-8 -*-
"""
IRIS - Smart Reply Suggestions
Lightweight, rule-based reply generation.
"""

import re


def generate_smart_replies(subject, body):
    """
    Generate three context-aware reply suggestions.

    Returns a list of three strings.
    Compatible with the existing function signature.
    """

    text = f"{subject or ''} {body or ''}".lower()
    text = re.sub(r"\s+", " ", text).strip()

    # 1. Email rejection
    if any(phrase in text for phrase in [
        "not selected", "unsuccessful", "application rejected",
        "regret to inform", "unfortunately, we cannot offer",
        "not moving forward", "position has been filled"
    ]):
        replies = [
            "Thank you for letting me know. I appreciate your consideration.",
            "Thank you for the opportunity. I wish your team all the best.",
            "I appreciate the update. Please keep me in mind for future opportunities."
        ]

    # 2. Interview invitation or scheduling
    elif any(word in text for word in [
        "interview", "recruitment", "shortlisted"
    ]):
        if any(phrase in text for phrase in [
            "reschedule", "rescheduled", "change the time",
            "different time", "another slot"
        ]):
            replies = [
                "Thank you for the update. Could you please share the available alternative slots?",
                "Thank you for informing me. I will check my availability and confirm shortly.",
                "I appreciate the update. Please let me know the revised schedule."
            ]
        elif any(phrase in text for phrase in [
            "confirm your availability", "please confirm",
            "let us know if you are available"
        ]):
            replies = [
                "Thank you for the invitation. I confirm my availability.",
                "Thank you for the update. The proposed time works for me.",
                "Thank you for considering my application. I look forward to the interview."
            ]
        else:
            replies = [
                "Thank you for the update. I appreciate you keeping me informed.",
                "Thank you for considering my application. I look forward to hearing from you.",
                "Thank you for the information. Please let me know if anything else is required."
            ]

    # 3. Job application update
    elif any(word in text for word in [
        "application", "internship", "job application", "position"
    ]):
        replies = [
            "Thank you for the update. I appreciate your consideration.",
            "Thank you for reviewing my application. I look forward to hearing from you.",
            "Thank you for the information. Please let me know if any further details are needed."
        ]

    # 4. Meeting, call, or appointment
    elif any(word in text for word in [
        "meeting", "client call", "appointment", "discussion", "schedule"
    ]):
        if any(phrase in text for phrase in [
            "cancelled", "canceled", "postponed", "rescheduled"
        ]):
            replies = [
                "Thank you for letting me know. Please share the updated schedule when available.",
                "Noted, thank you for the update. I will adjust my plans accordingly.",
                "Thank you for informing me. Please let me know if any action is needed from my side."
            ]
        elif any(phrase in text for phrase in [
            "confirm your availability", "please confirm", "are you available"
        ]):
            replies = [
                "Thank you for the update. I confirm my availability.",
                "Thanks for checking. The proposed time works for me.",
                "Thank you for reaching out. I will attend as scheduled."
            ]
        else:
            replies = [
                "Thank you for the update. I have noted the details.",
                "Thanks for letting me know. Please share any further details when available.",
                "Thank you for the information. I will get back to you if anything else is needed."
            ]

    # 5. Requests and assigned work
    elif any(word in text for word in [
        "please", "need you to", "required", "submit", "upload",
        "complete", "finish", "prepare", "deadline", "task"
    ]):
        replies = [
            "Thank you for letting me know. I will review the requirements.",
            "Noted. I will work on this and update you on my progress.",
            "Thank you for the details. I will let you know if I need any clarification."
        ]

    # 6. Project and review updates
    elif any(word in text for word in [
        "project", "presentation", "report", "review", "demo"
    ]):
        replies = [
            "Thank you for the update. I have noted the project details.",
            "Thanks for sharing this. I will review the information and follow up.",
            "Thank you for letting me know. I will update you on the next steps."
        ]

    # 7. General fallback
    else:
        replies = [
            "Thank you for your email. I appreciate the update.",
            "Thanks for sharing this information. I will review it and get back to you.",
            "Thank you for reaching out. Please let me know if there is anything else I should know."
        ]

    return replies
tests = [
    ("Application Rejected", "Unfortunately, your application was not selected."),
    ("Interview Rescheduled", "Your interview has been rescheduled. Please confirm the new time."),
    ("Project Deadline", "Please submit the project report by tomorrow."),
    ("General Update", "The documents have been received.")
]

for subject, body in tests:
    print(f"\n--- {subject} ---")
    for i, reply in enumerate(generate_smart_replies(subject, body), 1):
        print(f"{i}. {reply}")