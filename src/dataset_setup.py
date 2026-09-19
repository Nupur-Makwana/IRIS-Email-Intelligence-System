# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 08:18:38 2026

@author: nupur
"""

#STEP -1 : IMPORT DATA AND CHECK DATASET
'''
import kagglehub

# Download Enron Email Dataset
path = kagglehub.dataset_download("wcukierski/enron-email-dataset")
print("Path to dataset files:", path)'''

'''
import pandas as pd
dataset_path = r"E:\IRIS\dataset\emails.csv"
# Load dataset
df = pd.read_csv(dataset_path)
# Basic information
print("Dataset loaded successfully!")
print("Number of emails:", len(df))
print("Number of columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst 5 emails:")
print(df.head())'''

'''
import pandas as pd

dataset_path = r"E:\IRIS\dataset\emails.csv"

df = pd.read_csv(dataset_path)

print("Total emails:", len(df))
print("Columns:", df.columns.tolist())

print("\nFirst email:")
print(df.iloc[0])'''


#STEP -2 : Extract Subject, Sender, Receiver and Body
'''
import pandas as pd
import email
from email import policy

dataset_path = r"E:\IRIS\dataset\emails.csv"

# Load dataset
df = pd.read_csv(dataset_path)

print("Total emails:", len(df))


def parse_email(raw_message):
    try:
        msg = email.message_from_string(raw_message, policy=policy.default)

        sender = msg.get("From", "")
        receiver = msg.get("To", "")
        subject = msg.get("Subject", "")

        # Extract body
        if msg.is_multipart():
            body_parts = []

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body_parts.append(part.get_content())
                    except:
                        pass

            body = "\n".join(body_parts)

        else:
            try:
                body = msg.get_content()
            except:
                body = msg.get_payload()

        return sender, receiver, subject, body

    except Exception:
        return "", "", "", ""


# Test on first email
sender, receiver, subject, body = parse_email(df.iloc[0]["message"])

print("\n--- FIRST EMAIL ---")
print("Sender:", sender)
print("Receiver:", receiver)
print("Subject:", subject)
print("Body:", body[:500])
'''

#STEP - 3 : CLEAN DATASET
import pandas as pd
import email
from email import policy

dataset_path = r"E:\IRIS\dataset\emails.csv"

# Load only the raw data
df = pd.read_csv(dataset_path)

print("Total emails:", len(df))

# Take a random sample of 5000 emails
sample_df = df.sample(n=5000, random_state=42)

print("Emails selected for processing:", len(sample_df))


def parse_email(raw_message):
    try:
        msg = email.message_from_string(raw_message, policy=policy.default)

        sender = msg.get("From", "")
        receiver = msg.get("To", "")
        subject = msg.get("Subject", "")

        if msg.is_multipart():
            body_parts = []

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body_parts.append(part.get_content())
                    except:
                        pass

            body = "\n".join(body_parts)
        else:
            try:
                body = msg.get_content()
            except:
                body = msg.get_payload()

        return sender, receiver, subject, body

    except:
        return "", "", "", ""


emails = []

for i, message in enumerate(sample_df["message"]):

    sender, receiver, subject, body = parse_email(message)

    subject = str(subject).strip()
    body = str(body).strip()

    # Keep only emails with subject AND body
    if subject and body:

        emails.append({
            "email_id": f"E{i+1:06d}",
            "sender": sender,
            "receiver": receiver,
            "subject": subject,
            "body": body
        })


clean_df = pd.DataFrame(emails)

# Remove duplicates
clean_df = clean_df.drop_duplicates(subset=["subject", "body"])

print("\nUsable emails:", len(clean_df))

# Save
output_path = r"E:\IRIS\dataset\clean_emails.csv"
clean_df.to_csv(output_path, index=False)

print("\nSaved to:")
print(output_path)

print("\n--- SAMPLE SUBJECTS ---")
for subject in clean_df["subject"].sample(30, random_state=42):
    print("-", subject)