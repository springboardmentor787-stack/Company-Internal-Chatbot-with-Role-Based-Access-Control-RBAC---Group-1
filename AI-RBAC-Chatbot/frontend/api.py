import requests

BASE_URL = "http://127.0.0.1:8000"

def login_user(username, password):
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={"username": username, "password": password}
        )
        return response
    except:
        return None


def send_query(query, token):
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            params={"query": query},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return None

    except:
        return None
