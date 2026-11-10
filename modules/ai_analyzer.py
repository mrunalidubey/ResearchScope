
import re
import statistics


def analyze_ai_patterns(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 4]

    if len(sentences) < 5:
        return {
            "score": None,
            "message": "Not enough text for analysis.",
            "indicators": []
        }

    words_per_sentence = [len(s.split()) for s in sentences]

    average_length = statistics.mean(words_per_sentence)
    variation = statistics.pstdev(words_per_sentence)

    indicators = []
    score = 0

    if variation < 5:
        score += 25
        indicators.append("Very consistent sentence lengths")

    if average_length > 25:
        score += 15
        indicators.append("Long sentence structures")

    words = re.findall(r'\b\w+\b', text.lower())
    unique_ratio = len(set(words)) / max(len(words), 1)

    if unique_ratio < 0.35:
        score += 20
        indicators.append("Repeated vocabulary")

    score = min(score, 60)

    return {
        "score": score,
        "message": "Experimental writing-pattern estimate, not proof of AI use.",
        "indicators": indicators
    }
