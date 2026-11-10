
import re
from collections import Counter


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 6
    ]


def summarize_text(text, max_sentences=5):
    text = clean_text(text)
    sentences = split_sentences(text)

    if not sentences:
        return "Not enough readable text to generate a summary."

    stop_words = {
        "the", "is", "are", "was", "were", "a", "an", "and",
        "or", "of", "to", "in", "on", "for", "with", "by",
        "this", "that", "it", "as", "at", "be", "from",
        "we", "our", "their", "these", "those", "which"
    }

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    frequencies = Counter(
        word for word in words if word not in stop_words
    )

    scored_sentences = []

    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b', sentence.lower()
        )

        score = sum(
            frequencies[word] for word in sentence_words
        )

        score = score / max(len(sentence_words), 1)

        scored_sentences.append((index, score, sentence))

    top_sentences = sorted(
        scored_sentences,
        key=lambda item: item[1],
        reverse=True
    )[:max_sentences]

    top_sentences.sort(key=lambda item: item[0])

    return " ".join(item[2] for item in top_sentences)


def extract_section(text, keywords):
    sentences = split_sentences(text)

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            return sentence

    return "No clear information found in the extracted text."


def extract_keywords(text, count=10):
    stop_words = {
        "the", "is", "are", "was", "were", "a", "an",
        "and", "or", "of", "to", "in", "on", "for",
        "with", "by", "this", "that", "it", "as",
        "be", "from", "we", "our", "their", "which",
        "using", "based", "also", "can", "has", "have"
    }

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

    frequencies = Counter(
        word for word in words if word not in stop_words
    )

    return [word for word, frequency in frequencies.most_common(count)]


def analyze_paper(text):
    if not text or len(text.split()) < 30:
        return {
            "summary": "Not enough text to summarize.",
            "objective": "Not enough text available.",
            "methodology": "Not enough text available.",
            "findings": "Not enough text available.",
            "keywords": []
        }

    return {
        "summary": summarize_text(text),
        "objective": extract_section(
            text,
            ["objective", "aim of this study", "this paper proposes",
             "this study aims", "research objective"]
        ),
        "methodology": extract_section(
            text,
            ["methodology", "we propose", "we used",
             "experimental setup", "proposed method"]
        ),
        "findings": extract_section(
            text,
            ["results show", "our findings", "we found",
             "experimental results", "conclusion"]
        ),
        "keywords": extract_keywords(text)
    }
