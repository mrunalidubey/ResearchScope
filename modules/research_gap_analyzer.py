
import re


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 6
    ]


def analyze_research_gaps(text):

    sentences = split_sentences(text)

    limitation_terms = [
        "limitation", "limitations", "limited by",
        "constraint", "constraints", "challenge",
        "challenges", "drawback", "drawbacks"
    ]

    future_terms = [
        "future work", "future research",
        "further research", "future studies",
        "in future", "remains to be explored",
        "further investigation"
    ]

    limitations = []
    future_directions = []

    for sentence in sentences:
        lower_sentence = sentence.lower()

        if any(term in lower_sentence for term in limitation_terms):
            limitations.append(sentence)

        if any(term in lower_sentence for term in future_terms):
            future_directions.append(sentence)

    suggestions = []

    if limitations:
        suggestions.append({
            "title": "Investigate identified limitations",
            "description": (
                "Explore ways to address the limitations "
                "reported by the paper's authors."
            )
        })

    if future_directions:
        suggestions.append({
            "title": "Explore future research directions",
            "description": (
                "Investigate the future research areas "
                "suggested by the paper's authors."
            )
        })

    if not limitations and not future_directions:
        suggestions.append({
            "title": "Further literature investigation",
            "description": (
                "Review related studies to identify unanswered "
                "questions, conflicting findings and unexplored methods."
            )
        })

    return {
        "limitations": limitations[:5],
        "future_directions": future_directions[:5],
        "suggestions": suggestions
    }
