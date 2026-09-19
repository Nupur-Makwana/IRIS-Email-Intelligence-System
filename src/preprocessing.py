import pandas as pd
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# -----------------------------------
# 1. Load dataset
# -----------------------------------

file_path = r"E:\IRIS\dataset\priority_dataset.xlsx"

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")
print("Number of emails:", len(df))
print("\nColumns:")
print(df.columns.tolist())


# -----------------------------------
# 2. Download required NLTK resources
# -----------------------------------

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")


# -----------------------------------
# 3. Initialize NLP tools
# -----------------------------------

stop_words = set(stopwords.words("english"))

# Words that are important for email context
# and should NOT be removed.
important_words = {
    "am", "pm",
    "at", "on", "by",
    "before", "after",
    "during", "until",
    "from", "to",
    "over", "under",
    "between",
    "not", "no",
    "nor"
}

# Remove only stopwords that are NOT important
custom_stop_words = stop_words - important_words

lemmatizer = WordNetLemmatizer()


# -----------------------------------
# 4. Text preprocessing function
# -----------------------------------

def preprocess_text(text):

    # Convert to string
    text = str(text)

    # Lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Keep:
    # letters
    # numbers
    # spaces
    # colon (10:00)
    # slash (25/09/2026)
    # hyphen (25-09-2026)
    text = re.sub(r"[^a-zA-Z0-9\s:/\-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal
    tokens = [
        word for word in tokens
        if word not in custom_stop_words
    ]

    # Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    # Convert tokens back to text
    cleaned_text = " ".join(tokens)

    return cleaned_text


# -----------------------------------
# 5. Combine subject + body
# -----------------------------------

df["text"] = (
    df["subject"].fillna("") +
    " " +
    df["body"].fillna("")
)


# -----------------------------------
# 6. Apply preprocessing
# -----------------------------------

print("\nPreprocessing emails...")

df["clean_text"] = df["text"].apply(preprocess_text)


# -----------------------------------
# 7. Display examples
# -----------------------------------

print("\nSample preprocessing results:\n")

for i in range(5):

    print("Original:")
    print(df.loc[i, "text"])

    print("\nCleaned:")
    print(df.loc[i, "clean_text"])

    print("\nPriority:", df.loc[i, "priority"])
    print("-" * 70)


# -----------------------------------
# 8. Save processed dataset
# -----------------------------------

output_path = r"E:\IRIS\dataset\priority_dataset_processed.csv"

df.to_csv(output_path, index=False)

print("\nPreprocessing completed successfully!")
print("Saved to:")
print(output_path)