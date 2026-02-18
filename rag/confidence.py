def calculate_confidence(results):
    if not results:
        return 0.0

    distances = [score for _, score in results]

    best = min(distances)
    worst = max(distances)

    # Measure how much better best result is compared to others
    spread = worst - best

    # If spread small → low confidence
    if spread < 0.02:
        return 0.4  # moderate flat confidence

    # Otherwise scale based on spread
    confidence = spread * 5  # amplify small spreads

    confidence = max(0.3, min(confidence, 0.95))

    return round(confidence, 2)
