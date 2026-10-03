import re
import nltk
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt", quiet=True)


def split_sentences(text):
    """
    Split email body into individual sentences.
    """

    text = re.sub(r'([.!?])(?=[A-Z])', r'\1 ', text)
    text = re.sub(r',(?=I\s)', ', ', text)

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def has_date_or_time(sentence):
    """
    Detect dates, times and common temporal expressions.
    """

    pattern = re.compile(
        r"""
        (
            # Numeric dates: 28/09/26, 28-09-2026
            \b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b

            |

            # Written dates: 28 September 2026
            \b\d{1,2}\s+
            (?:January|February|March|April|May|June|July|August|
            September|October|November|December)
            (?:\s+\d{2,4})?\b

            |

            # Time: 10:00 AM, 14:30
            \b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b

            |

            # Time: 2 PM
            \b\d{1,2}\s*(?:AM|PM|am|pm)\b

            |

            # Relative dates
            \b(?:today|tomorrow|tonight|yesterday)\b

            |

            # Weekdays
            \b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b
        )
        """,
        re.IGNORECASE | re.VERBOSE
    )

    return bool(pattern.search(sentence))


def has_deadline_or_action(sentence):
    """
    Detect deadline, submission and action-related information.
    """

    keywords = [
        "deadline",
        "due",
        "submit",
        "submission",
        "confirm",
        "confirmation",
        "respond",
        "response",
        "required",
        "must",
        "need to",
        "please",
        "action required",
        "complete",
        "register",
        "apply",
        "attend",
        "contact",
        "reply",
        "prepare",
        "review"
    ]

    sentence_lower = sentence.lower()

    return any(
        keyword in sentence_lower
        for keyword in keywords
    )


def has_event_information(sentence):
    """
    Detect sentences describing meetings, interviews,
    appointments or scheduled events.
    """

    keywords = [
        "meeting",
        "interview",
        "appointment",
        "scheduled",
        "schedule",
        "review",
        "session",
        "presentation",
        "event",
        "call"
    ]

    sentence_lower = sentence.lower()

    return any(
        keyword in sentence_lower
        for keyword in keywords
    )


def calculate_textrank_scores(sentences):
    """
    Calculate TextRank scores using sentence similarity.
    """

    if len(sentences) == 1:
        return np.array([1.0])

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(sentences)

    similarity_matrix = cosine_similarity(matrix)

    # Remove similarity of a sentence with itself
    np.fill_diagonal(similarity_matrix, 0)

    row_sums = similarity_matrix.sum(axis=1)

    # Prevent division by zero
    row_sums[row_sums == 0] = 1

    normalized_matrix = (
        similarity_matrix / row_sums[:, None]
    )

    # PageRank-style TextRank
    scores = np.ones(len(sentences))

    damping = 0.85

    for _ in range(50):

        new_scores = (
            (1 - damping)
            + damping * normalized_matrix.T.dot(scores)
        )

        if np.allclose(scores, new_scores):
            break

        scores = new_scores

    return scores


def summarize_email(subject, body, max_sentences=None):
    """
    Generate an extractive email summary using:

    1. TextRank
    2. Date/time awareness
    3. Deadline/action awareness
    4. Meeting/event awareness

    Short emails use 2 sentences.
    Longer emails can use up to 3 sentences.
    """

    # Only summarize the email body.
    # The subject should not appear as a summary sentence.
    text = str(body)

    sentences = split_sentences(text)

    if not sentences:
        return ""

    # -----------------------------------------
    # Determine summary length
    # -----------------------------------------

    if max_sentences is None:

        if len(sentences) >= 6:
            max_sentences = 3
        else:
            max_sentences = 2

    # If the email is already short,
    # return the complete body.
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    # -----------------------------------------
    # Step 1: TextRank
    # -----------------------------------------

    scores = calculate_textrank_scores(sentences)

    # -----------------------------------------
    # Step 2: Email-specific importance
    # -----------------------------------------

    for i, sentence in enumerate(sentences):

        contains_date = has_date_or_time(sentence)
        contains_action = has_deadline_or_action(sentence)
        contains_event = has_event_information(sentence)

        # Strong bonus for dates/times
        if contains_date:
            scores[i] += 0.40

        # Bonus for actions/deadlines
        if contains_action:
            scores[i] += 0.25

        # Extra bonus when a sentence contains
        # both event information and a date/time.
        if contains_date and contains_event:
            scores[i] += 0.35

        # Extra importance for explicit deadline sentences
        sentence_lower = sentence.lower()

        if any(
            word in sentence_lower
            for word in [
                "deadline",
                "due",
                "submit",
                "submission",
                "must be submitted"
            ]
        ):
            scores[i] += 0.20

    # -----------------------------------------
    # Step 3: Select important sentences
    # -----------------------------------------

    ranked_indices = np.argsort(scores)[::-1]

    selected_indices = []

    # First prioritize sentences containing
    # important dates/events/deadlines.
    important_indices = [
        i for i in ranked_indices
        if (
            has_date_or_time(sentences[i])
            or has_deadline_or_action(sentences[i])
        )
    ]

    for i in important_indices:

        if i not in selected_indices:
            selected_indices.append(i)

        if len(selected_indices) >= max_sentences:
            break

    # Fill remaining slots with TextRank results
    if len(selected_indices) < max_sentences:

        for i in ranked_indices:

            if i not in selected_indices:
                selected_indices.append(i)

            if len(selected_indices) >= max_sentences:
                break

    # -----------------------------------------
    # Step 4: Restore original email order
    # -----------------------------------------

    selected_indices = sorted(selected_indices)

    summary = " ".join(
        sentences[i]
        for i in selected_indices
    )

    return summary