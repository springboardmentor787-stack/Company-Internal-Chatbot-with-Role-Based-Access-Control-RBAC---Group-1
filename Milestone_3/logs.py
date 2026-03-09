from milestone_3.database import get_db


def log_access(
    username: str,
    role: str,
    query: str,
    confidence: float,
    response_time: float
):
    """
    Logs user access into access_logs table.
    """

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO access_logs
        (username, role, query, confidence, response_time)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        role,
        query,
        confidence,
        response_time
    ))

    conn.commit()
    conn.close()