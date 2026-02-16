import requests

BASE_URL = "http://127.0.0.1:8000"


# ==============================
# LOGIN FUNCTION
# ==============================
def login_user(username: str, password: str):
    """
    Calls FastAPI /login endpoint
    Returns JSON response or error
    """

    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("detail", "Login failed")}

    except Exception as e:
        return {"error": str(e)}


# ==============================
# CHAT FUNCTION (RAG)
# ==============================
def send_chat_message(token: str, message: str):
    """
    Calls FastAPI /rag-chunks endpoint
    """

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "query": message
    }

    try:
        response = requests.post(
            f"{BASE_URL}/rag-chunks",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.json().get("detail", "Chat request failed")
            }

    except Exception as e:
        return {"error": str(e)}
