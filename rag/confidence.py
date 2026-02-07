def calculate_confidence(results):
    if not results:
        return 1.0

    scores = [score for _, score in results]
    avg_score = sum(scores) / len(scores)

    # Convert similarity score → confidence
    confidence = max(0.0, min(1.0, 1 - avg_score))
    return round(confidence, 2)
