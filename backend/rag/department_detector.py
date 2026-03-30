# department_detector.py

DEPT_KEYWORDS = {
    "hr": [
        "leave", "salary", "attendance", "benefits", "policy",
        "employee", "joining", "appraisal", "promotion"
    ],

    "finance": [
        "budget", "revenue", "profit", "expense", "tax",
        "financial", "quarterly", "report", "income"
    ],

    "marketing": [
        "campaign", "brand", "leads", "ads", "promotion",
        "market", "customer", "engagement", "sales"
    ],

    "engineering": [
        "system", "api", "authentication", "backend",
        "architecture", "database", "security", "server"
    ],

    "general": [
        "policy", "handbook", "rules", "guidelines",
        "company", "conduct", "security"
    ]
}


def detect_department(question: str) -> str | None:
    """
    Detect department from question keywords
    """

    q = question.lower()

    scores = {}

    for dept, keywords in DEPT_KEYWORDS.items():

        count = 0

        for word in keywords:
            if word in q:
                count += 1

        scores[dept] = count

    # Find best match
    best_dept = max(scores, key=scores.get)

    if scores[best_dept] == 0:
        return None

    return best_dept
