
import html
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# 1. EMAIL CLEANING
# ---------------------------------------------------------

def clean_email_body(body):
    """Remove HTML, greetings, signatures, and common email footers."""

    if not body:
        return ""

    text = html.unescape(str(body))
    text = text.replace("\xa0", " ")

    # Convert common HTML formatting into sentence boundaries.
    text = re.sub(
        r"(?i)<\s*(br|/p|/div|/li|/tr|/h[1-6])\s*/?\s*>",
        "\n",
        text,
    )

    # Remove remaining HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace.
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.splitlines()
    ]

    cleaned_lines = []

    footer_patterns = [
        r"^sent from my\b",
        r"^this email and any attachments\b",
        r"^confidentiality notice\b",
        r"^unsubscribe\b",
        r"^to unsubscribe\b",
        r"^view this email in your browser\b",
        r"^please consider the environment\b",
    ]

    signoff_patterns = [
        r"^(kind regards|best regards|warm regards|regards|"
        r"thanks and regards|many thanks|thank you|sincerely|"
        r"best wishes|cheers)[,!.\s]*$",
    ]

    signature_patterns = [
        r"^(recruitment team|hr team|human resources team)\b",
        r"^customer support\b",
        r"^support team\b",
        r"^sent by\b",
        r"^www\.",
        r"^https?://",
        r"^phone\s*:",
        r"^email\s*:",
        r"^address\s*:",
    ]

    for line in lines:
        if not line:
            continue

        lower = line.lower().strip()

        # Stop reading when a conventional footer begins.
        if any(re.search(pattern, lower) for pattern in footer_patterns):
            break

        # Stop at a standalone sign-off.
        if any(re.match(pattern, lower) for pattern in signoff_patterns):
            break

        # Skip common signature lines.
        if any(re.match(pattern, lower) for pattern in signature_patterns):
            continue

        # Remove a greeting at the beginning of a line.
        line = re.sub(
            r"(?i)^(hi|hello|dear)\s+"
            r"[\w .'-]{1,40}[,!:\-]\s*",
            "",
            line,
        ).strip()

        if line:
            cleaned_lines.append(line)

    text = " ".join(cleaned_lines)

    # Remove a greeting joined to the beginning of a message.
    text = re.sub(
        r"(?i)^(hi|hello|dear)\s+"
        r"[\w .'-]{1,40}[,!:\-]\s*",
        "",
        text,
    ).strip()

    # Remove inline sign-offs followed by a name.
    text = re.sub(
        r"(?i)\s+(kind regards|best regards|warm regards|"
        r"regards|sincerely|best wishes)\s*[,!]?.*$",
        "",
        text,
    ).strip()

    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------
# 2. SENTENCE SPLITTING
# ---------------------------------------------------------

def split_sentences(text):
    """Split text into sentences while avoiding common abbreviations."""

    if not text:
        return []

    text = re.sub(r"\s+", " ", text).strip()

    # Protect common abbreviations and titles from premature splitting.
    protected = {
        "Mr.": "Mr<prd>",
        "Mrs.": "Mrs<prd>",
        "Ms.": "Ms<prd>",
        "Dr.": "Dr<prd>",
        "Prof.": "Prof<prd>",
        "Sr.": "Sr<prd>",
        "Jr.": "Jr<prd>",
        "e.g.": "e<prd>g<prd>",
        "i.e.": "i<prd>e<prd>",
        "vs.": "vs<prd>",
        "U.S.": "U<prd>S<prd>",
        "A.M.": "A<prd>M<prd>",
        "P.M.": "P<prd>M<prd>",
    }

    for original, replacement in protected.items():
        text = text.replace(original, replacement)
        text = text.replace(original.lower(), replacement.lower())

    parts = re.split(r"(?<=[.!?])\s+", text)

    sentences = []

    for part in parts:
        part = part.replace("<prd>", ".").strip()

        if part:
            sentences.append(part)

    return sentences


# ---------------------------------------------------------
# 3. LOW-VALUE SENTENCE FILTERING
# ---------------------------------------------------------

def is_low_value_sentence(sentence):
    """Identify generic promotional and low-information sentences."""

    text = sentence.lower().strip()

    low_value_patterns = [
        r"^hope you are doing well[.! ]*$",
        r"^i hope you are doing well[.! ]*$",
        r"^hope this email finds you well[.! ]*$",
        r"^i hope this email finds you well[.! ]*$",
        r"^have a great day[.! ]*$",
        r"^thank you for your time[.! ]*$",
        r"^please do not hesitate to contact us[.! ]*$",
        r"^we appreciate your interest[.! ]*$",
        r"^stay tuned for more updates[.! ]*$",
    ]

    if any(re.match(pattern, text) for pattern in low_value_patterns):
        return True

    # Filter generic marketing sentences only when they have no
    # concrete product, event, deadline, or customer action.
    promotional_phrases = [
        "shop now",
        "browse our store",
        "discover our collection",
        "don't miss out",
        "exclusive offers",
        "limited time offer",
        "seasonal offers",
    ]

    contains_concrete_information = any(
        marker in text
        for marker in [
            "by ",
            "deadline",
            "due ",
            "tomorrow",
            "today",
            "register",
            "registration",
            "event",
            "meeting",
            "appointment",
            "interview",
            "price",
            "discount",
            "order",
            "delivery",
            "required",
            "must ",
        ]
    )

    if (
        any(phrase in text for phrase in promotional_phrases)
        and not contains_concrete_information
    ):
        return True

    return False


# ---------------------------------------------------------
# 4. WORD AND SCORE UTILITIES
# ---------------------------------------------------------

def get_words(text):
    """Return normalized words for overlap calculations."""

    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def normalize_scores(scores):
    """Normalize numeric scores into the range 0 to 1."""

    scores = np.asarray(scores, dtype=float)

    if len(scores) == 0:
        return scores

    minimum = float(np.min(scores))
    maximum = float(np.max(scores))

    if maximum - minimum < 1e-10:
        return np.zeros_like(scores)

    return (scores - minimum) / (maximum - minimum)


def calculate_textrank_scores(sentences):
    """Calculate lightweight TextRank-style sentence importance."""

    count = len(sentences)

    if count == 0:
        return np.array([])

    if count == 1:
        return np.array([1.0])

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=3000,
        )

        matrix = vectorizer.fit_transform(sentences)

        similarity = cosine_similarity(matrix)
        np.fill_diagonal(similarity, 0)

        row_sums = similarity.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1

        transition = similarity / row_sums

        # Simple iterative ranking.
        scores = np.ones(count) / count
        damping = 0.85

        for _ in range(30):
            scores = (
                (1 - damping) / count
                + damping * transition.T.dot(scores)
            )

        return scores

    except ValueError:
        return np.ones(count)


def calculate_subject_relevance(subject, sentences):
    """Score sentence relevance to the email subject."""

    if not subject or not sentences:
        return np.zeros(len(sentences))

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=3000,
        )

        documents = [subject] + sentences
        matrix = vectorizer.fit_transform(documents)

        subject_vector = matrix[0:1]
        sentence_vectors = matrix[1:]

        scores = cosine_similarity(
            sentence_vectors,
            subject_vector,
        ).flatten()

        return scores

    except ValueError:
        return np.zeros(len(sentences))


# ---------------------------------------------------------
# 5. CONTENT DETECTION
# ---------------------------------------------------------

def has_main_event(sentence):
    """Detect important events, updates, and decisions."""

    text = sentence.lower()

    patterns = [
        r"\binterview\b",
        r"\bmeeting\b",
        r"\bappointment\b",
        r"\bcall\b",
        r"\breview\b",
        r"\bdeadline\b",
        r"\breport\b",
        r"\bsubmission\b",
        r"\bflight\b",
        r"\btravel\b",
        r"\btest results?\b",
        r"\bpayment\b",
        r"\bchargeback\b",
        r"\baccount\b",
        r"\bsecurity alert\b",
        r"\bapplication\b",
        r"\bregistration\b",
        r"\bhackathon\b",
        r"\binspection\b",
        r"\bproject\b",
        r"\bvisa appointment\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def has_action(sentence):
    """Detect instructions, requests, and required actions."""

    text = sentence.lower()

    patterns = [
        r"\bplease\b",
        r"\bconfirm\b",
        r"\bsubmit\b",
        r"\bupload\b",
        r"\bsend\b",
        r"\bshare\b",
        r"\bcontact\b",
        r"\bcall\b",
        r"\bcheck\b",
        r"\bcomplete\b",
        r"\bfinish\b",
        r"\bprovide\b",
        r"\brespond\b",
        r"\breply\b",
        r"\breset\b",
        r"\bchange\b",
        r"\bbook\b",
        r"\bregister\b",
        r"\battend\b",
        r"\bpush\b",
        r"\bmerge\b",
        r"\bhandle\b",
        r"\bprepare\b",
        r"\barrange\b",
        r"\bverify\b",
        r"\bupdate\b",
        r"\bpay\b",
        r"\battach\b",
        r"\bapprove\b",
        r"\breject\b",
        r"\bstep in\b",
        r"\btake care of\b",
        r"\blook into\b",
        r"\bfollow up\b",
        r"\bdo this\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def has_direct_request(sentence):
    """Give extra weight to explicit requests or delegation."""

    text = sentence.lower().strip()

    request_patterns = [
        r"\bcould you\b",
        r"\bcan you\b",
        r"\bwould you\b",
        r"\bwill you\b",
        r"\bplease\b",
        r"\bi need you to\b",
        r"\bi'd like you to\b",
        r"\bi would like you to\b",
        r"\bwould you mind\b",
        r"\bcan someone\b",
        r"\bcould someone\b",
        r"\bplease help\b",
        r"\bstep in\b",
        r"\bhandle it\b",
        r"\bcover for me\b",
        r"\btake over\b",
        r"\btake care of\b",
    ]

    return any(re.search(pattern, text) for pattern in request_patterns)


def has_deadline(sentence):
    """Detect explicit or relative dates and time constraints."""

    text = sentence.lower()

    patterns = [
        r"\bby\s+\d{1,2}(:\d{2})?\s*(am|pm)?\b",
        r"\bby\s+(today|tomorrow|tonight|monday|tuesday|wednesday|"
        r"thursday|friday|saturday|sunday)\b",
        r"\bdue\s+(today|tomorrow|tonight)\b",
        r"\bdue\s+on\b",
        r"\bdeadline\b",
        r"\bbefore\s+\d{1,2}(:\d{2})?\s*(am|pm)?\b",
        r"\bwithin\s+\d+\s+(hour|hours|day|days|minute|minutes)\b",
        r"\btonight\b",
        r"\btomorrow morning\b",
        r"\btomorrow afternoon\b",
        r"\btomorrow evening\b",
        r"\b\d{1,2}(:\d{2})\s*(am|pm)\b",
        r"\b\d{1,2}\s*(am|pm)\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def has_context(sentence):
    """Detect supporting information that explains an event."""

    text = sentence.lower()

    patterns = [
        r"\bbecause\b",
        r"\bso that\b",
        r"\btherefore\b",
        r"\bwhich means\b",
        r"\bas a result\b",
        r"\bif this was not you\b",
        r"\botherwise\b",
        r"\bif not\b",
        r"\bso you are prepared\b",
        r"\bwill not be reachable\b",
        r"\bnot be available\b",
        r"\bmay not be accepted\b",
        r"\bwill be offered to another\b",
    ]

    return any(re.search(pattern, text) for pattern in patterns)


def calculate_sentence_bonus(sentence, index):
    """Add importance bonuses for useful email information."""

    score = 0.0

    if has_main_event(sentence):
        score += 0.20

    if has_action(sentence):
        score += 0.20

    if has_deadline(sentence):
        score += 0.20

    if has_context(sentence):
        score += 0.12

    # New: prioritize explicit requests and delegation.
    if has_direct_request(sentence):
        score += 0.35

    # A small first-sentence bonus helps preserve opening context.
    if index == 0:
        score += 0.03

    return score


# ---------------------------------------------------------
# 6. REDUNDANCY CHECK
# ---------------------------------------------------------

def word_overlap(sentence_a, sentence_b):
    """Calculate Jaccard overlap between two sentences."""

    words_a = set(get_words(sentence_a))
    words_b = set(get_words(sentence_b))

    if not words_a or not words_b:
        return 0.0

    union = words_a | words_b

    if not union:
        return 0.0

    return len(words_a & words_b) / len(union)


# ---------------------------------------------------------
# 7. MAIN SUMMARIZATION FUNCTION
# ---------------------------------------------------------

def summarize_email(subject, body, max_sentences=None):
    """
    Summarize an email using sentence ranking and content-aware scoring.

    Keep this signature compatible with the existing IRIS backend.
    """

    cleaned = clean_email_body(body)
    sentences = split_sentences(cleaned)

    # Remove empty and low-value sentences.
    sentences = [
        sentence
        for sentence in sentences
        if sentence.strip() and not is_low_value_sentence(sentence)
    ]

    if not sentences:
        return ""

    if max_sentences is None:
        max_sentences = 2

    try:
        max_sentences = int(max_sentences)
    except (TypeError, ValueError):
        max_sentences = 2

    max_sentences = max(1, max_sentences)

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    rank_scores = normalize_scores(
        calculate_textrank_scores(sentences)
    )

    subject_scores = normalize_scores(
        calculate_subject_relevance(subject, sentences)
    )

    # Base score from sentence importance and subject relevance.
    scores = (
        0.35 * rank_scores
        + 0.25 * subject_scores
    )

    # Add content-specific importance bonuses.
    for index, sentence in enumerate(sentences):
        scores[index] += calculate_sentence_bonus(sentence, index)

    # Select sentences by score while avoiding redundancy.
    ranked_indices = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True,
    )

    selected_indices = []

    for index in ranked_indices:
        candidate = sentences[index]

        too_similar = any(
            word_overlap(candidate, sentences[selected_index]) >= 0.70
            for selected_index in selected_indices
        )

        if too_similar:
            continue

        selected_indices.append(index)

        if len(selected_indices) >= max_sentences:
            break

    # Preserve original reading order.
    selected_indices.sort()

    summary = " ".join(
        sentences[index]
        for index in selected_indices
    )

    return summary.strip()
