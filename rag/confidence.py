def calculate_confidence(results):
    if not results:
        return 0.0

    scores = [score for _, score in results]
    best_score = min(scores)

    # Define realistic min/max distance range
    MIN_DIST = 0.70   # strong match
    MAX_DIST = 0.90   # weak match

    # Normalize
    confidence = 1 - ((best_score - MIN_DIST) / (MAX_DIST - MIN_DIST))

    confidence = max(0.0, min(confidence, 1.0))

    return round(confidence, 2)
