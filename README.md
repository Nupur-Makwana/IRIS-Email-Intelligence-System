# IRIS – Intelligent Email Analysis System

IRIS is an intelligent email analysis system that uses Natural Language Processing (NLP) and Machine Learning to automatically analyze emails, determine their priority, classify them into categories, and generate concise summaries.

The system combines NLP techniques with a FastAPI backend and MySQL database to provide an integrated email management platform.

---

## 📌 Project Overview

Managing a large number of emails can make it difficult to identify important messages, understand lengthy content, and organize emails efficiently.

IRIS aims to reduce this effort by automatically analyzing emails and providing useful information such as:

- Email priority
- Email category
- AI-generated summary
- Intelligent email management

The current implementation focuses mainly on:

1. Priority Classification
2. Category Classification
3. Email Summarization
4. Backend Email Management
5. User Authentication

Additional intelligent features are being developed as part of the project.

---

## 🎯 Objectives

The main objectives of IRIS are:

- Automatically identify the priority of an email.
- Classify emails into meaningful categories.
- Generate concise summaries of email content.
- Apply NLP techniques to real-world email text.
- Compare different machine-learning models.
- Integrate NLP models with a functional backend.
- Provide secure user authentication.
- Store and manage emails using a database.
- Build a foundation for intelligent email-management features.

---

## ✨ Current Features

### 📊 Priority Classification

Emails are classified into three priority levels:

- HIGH
- MEDIUM
- LOW

Two machine-learning models were evaluated:

- Multinomial Naive Bayes
- Logistic Regression

The final priority prediction pipeline uses **Multinomial Naive Bayes**.

Test accuracy:

**94.00%**

---

### 🏷️ Category Classification

Emails are automatically classified into categories such as:

- Academic
- Job/Internship
- Work/Project
- Meeting/Appointment
- Personal
- Travel
- Technology
- Financial
- Security
- Newsletter
- Promotion
- Entertainment
- Food/Lifestyle
- Community
- Legal/Administrative
- Event
- Service
- Other

Two models were compared:

- Multinomial Naive Bayes
- Logistic Regression

The final category prediction pipeline uses **Logistic Regression**.

Test accuracy:

**72.67%**

---

### 📝 Email Summarization

IRIS uses a lightweight extractive summarization approach.

The system:

1. Splits the email into sentences.
2. Calculates TF-IDF scores for the sentences.
3. Ranks sentences according to their importance.
4. Selects the most important sentences.
5. Generates a short summary.

The approach runs locally and does not require a large pretrained language model.

Summarization evaluation was performed using:

- ROUGE-1
- ROUGE-2
- ROUGE-L

Evaluation results:

| Metric | Score |
|---|---:|
| ROUGE-1 | 0.4770 |
| ROUGE-2 | 0.2818 |
| ROUGE-L | 0.4172 |

---

## 🧠 NLP Pipeline

The main NLP pipeline is:

```text
Email
  ↓
Text Extraction
  ↓
Data Cleaning
  ↓
Lowercasing
  ↓
Tokenization
  ↓
Stop-word Removal
  ↓
Lemmatization
  ↓
TF-IDF Feature Extraction
  ↓
Unigrams + Bigrams
  ↓
 ┌──────────────────┬───────────────────┐
 ↓                  ↓                   ↓
Priority          Category          Summarization
Classification    Classification
 ↓                  ↓                   ↓
HIGH/MEDIUM/LOW   Email Category     Short Summary

## Machine Learning
Priority Classification

Models evaluated:

Multinomial Naive Bayes

Logistic Regression

Multinomial Naive Bayes was selected for the final priority prediction pipeline based on the test results.

Logistic Regression was selected for the final category prediction pipeline.

---

## Dataset

Main Classification Dataset

A curated synthetic email dataset containing:

750 emails

Priority	Emails
HIGH	250
MEDIUM	250
LOW	250
Total	750

Dataset fields include:

email_id
sender
receiver
subject
body
category
priority
source

The dataset was divided using an 80:20 stratified split:

Training: 600 emails
Testing: 150 emails
Summarization Dataset

A separate evaluation set containing:

20 emails with human-written reference summaries

was used to evaluate the summarization component using ROUGE metrics.

Enron Dataset

The Enron Email Dataset was also explored as a supplementary real-world email corpus.

It was not used as the main supervised priority dataset because suitable priority labels were not available for the project.

---

## Technologies Used

Programming Language
Python
NLP & Machine Learning
NLTK
Scikit-learn
Pandas
NumPy
Matplotlib
Joblib
Backend
FastAPI
Uvicorn
Database
MySQL
SQLAlchemy
PyMySQL
Authentication & Security
JWT
python-jose
Passlib
bcrypt
HTTP Bearer Authentication
Configuration
python-dotenv
Evaluation
ROUGE
Development Tools
Spyder
Anaconda
Git
GitHub

---

## System Architecture

                  ┌───────────────────┐
                  │       User        │
                  └─────────┬─────────┘
                            ↓
                  ┌───────────────────┐
                  │ IRIS Application  │
                  └─────────┬─────────┘
                            ↓
                  ┌───────────────────┐
                  │   FastAPI Backend │
                  └─────────┬─────────┘
                            ↓
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │ Priority   │ │ Category   │ │ Summarizer │
      │ Classifier │ │ Classifier │ │            │
      └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                 ┌───────────────────┐
                 │ Email AI Analysis │
                 └─────────┬─────────┘
                           ↓
                 ┌───────────────────┐
                 │   MySQL Database  │
                 └───────────────────┘

## Authentication

IRIS uses JWT-based authentication.

The authentication flow is:

User Registration
       ↓
Password Hashing
       ↓
User Stored in Database
       ↓
User Login
       ↓
JWT Access Token
       ↓
Bearer Authentication
       ↓
Protected API Endpoints

Passwords are hashed using bcrypt before being stored.

Sensitive configuration such as database credentials and the JWT secret is stored in environment variables rather than directly in the source code.

## Backend API

The FastAPI backend currently provides endpoints for authentication, email management, health checks, and AI processing.

Examples include:

POST /auth/register
POST /auth/login

POST /emails/send
GET  /emails/inbox

POST /ai/summarize

GET /health
GET /database-test

The API can be tested through the FastAPI Swagger interface.

## Project Structure
IRIS/
│
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── auth.py
│       ├── security.py
│       ├── emails.py
│       ├── ai.py
│       └── .env
│
├── dataset/
│   ├── priority_dataset.xlsx
│   ├── priority_dataset_processed.csv
│   ├── category_dataset_processed.csv
│   ├── summarization_evaluation.csv
│   └── clean_emails.csv
│
├── models/
│   ├── priority_nb_model.pkl
│   ├── priority_tfidf_vectorizer.pkl
│   ├── category_lr_model.pkl
│   └── category_tfidf_vectorizer.pkl
│
├── results/
│   ├── priority_model_comparison.png
│   ├── priority_confusion_matrix.png
│   ├── category_model_comparison.png
│   ├── category_confusion_matrix_lr.png
│   ├── priority_class_distribution.png
│   ├── category_class_distribution.png
│   ├── summarization_rouge_scores.png
│   └── summarization_metrics.csv
│
├── src/
│   ├── preprocessing.py
│   ├── tfidf_features.py
│   ├── priority_classifier.py
│   ├── train_naive_bayes.py
│   ├── train_logistic_regression.py
│   ├── save_priority_model.py
│   ├── predict_priority.py
│   ├── clean_categories.py
│   ├── train_category_models.py
│   ├── predict_category.py
│   ├── summarization.py
│   ├── priority_error_analysis.py
│   └── category_error_analysis.py
│
├── .gitignore
└── README.md

## Privacy and Security

The current backend includes:

Password hashing
JWT authentication
Bearer token authentication
Environment-based configuration
Protected backend endpoints

Future versions can include stronger privacy-preserving and encryption mechanisms.

## Current Development Status
# Completed
 Dataset preparation
 Text preprocessing
 TF-IDF feature extraction
 Priority classification
 Category classification
 Email summarization
 Model evaluation
 Error analysis
 FastAPI backend
 MySQL database integration
 User registration
 User login
 JWT authentication
 Email sending
 Inbox
 Read/unread functionality
 Automatic priority, category and summary generation

# In Development
 Smart replies
 Explainable priority
 Frontend interface
 Intelligent reminders
 Opportunity detection
 Smart email management
 Additional personalization features

## Future Scope

Future versions of IRIS can include:

Larger real-world labelled email datasets
Advanced summarization models
Personalized priority prediction
Smart reply generation
Behaviour-based email organization
Smart email cleanup with user approval
Automatic reminders for important events
Job and internship opportunity detection
Improved category classification
Stronger privacy and encryption mechanisms
A complete production-ready web interface

##  Research Focus

The project focuses on applying Natural Language Processing to email management, particularly:

Email priority classification
Email category classification
Email summarization
Traditional NLP and machine-learning methods
Lightweight local NLP processing

## Author

Nupur Makwana

BCA – Department of Computer Applications

## This project is developed for academic and educational purposes.
