# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 12:48:10 2026

@author: nupur
"""


from summarization import clean_email_body, summarize_email

# Replace these examples with the exact raw email bodies
# from your evaluation dataset if the wording differs.
tests = {
    "M101": """
    Thanks for applying to the Frontend Intern role.
    Our team is going through applications this month and will
    reach out to shortlisted candidates with next steps once the
    review is complete.
    Recruitment Team, Nexova Technologies
    """,
    "H081": """
    Dad's flight back got cancelled because of the weather and
    he is stuck at the airport with no clear rebooking yet.
    Can you check flights from your end too, in case we find
    something faster than what the airline is offering him?
    """
}

for email_id, body in tests.items():
    print(f"\n--- {email_id} ---")
    print("CLEANED BODY:")
    print(clean_email_body(body))
    print("GENERATED SUMMARY:")
    print(summarize_email(email_id, body))

print("\n--- THREE-SENTENCE SELECTION TEST ---")

test_subject = "Interview Slot Confirmation"

test_body = (
    "I hope you are doing well and having a good week. "
    "Your interview is scheduled for Thursday at 10 AM. "
    "Please confirm your availability by 6 PM today or the slot "
    "will be offered to another candidate."
)

print("GENERATED SUMMARY:")
print(summarize_email(test_subject, test_body))

extra_tests = [
    (
        "URGENT DEADLINE",
        "Project Report Submission",
        "Hope you are doing well. The final report is due tomorrow "
        "at 9 AM. Please upload the report tonight or your submission "
        "may not be accepted."
    ),
    (
        "SECURITY ALERT",
        "Suspicious Account Activity",
        "We detected a login from an unfamiliar device. "
        "If this was not you, reset your password immediately "
        "and contact support to secure your account."
    ),
    (
        "PROMOTIONAL EMAIL",
        "Weekend Store Offers",
        "Our weekend collection has arrived with fresh styles. "
        "Browse the store for new arrivals and seasonal offers."
    ),
]

for name, subject, body in extra_tests:
    print(f"\n--- {name} ---")
    print(summarize_email(subject, body))
print("\n--- ACTION-AWARE SELECTION TEST ---")

subject = "Client Call Coverage"

body = (
    "Something has come up with my visa appointment "
    "and I will not be reachable during tomorrow's client call. "
    "Could you step in and handle it? "
    "I will send you my notes tonight so you are prepared."
)

print(summarize_email(subject, body))