import os
import requests

def get_token_stateless():
    """Get LINE access token."""
    endpoint = "https://api.line.me/oauth2/v3/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("CHANNEL_ID"),
        "client_secret": os.getenv("CHANNEL_SECRET"),
    }
    response = requests.post(endpoint, data=data)
    response.raise_for_status()
    result = response.json()
    return result.get("access_token", "")

def reply_message(reply_token, messages):
    """Send a reply message via LINE."""
    if not isinstance(messages, list):
        messages = [messages]

    access_token = get_token_stateless()
    endpoint = "https://api.line.me/v2/bot/message/reply"
    payload = {
        "replyToken": reply_token,
        "messages": messages,
    }
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()

def loading_message(line_user_id):
    """Send a loading message."""
    access_token = get_token_stateless()
    endpoint = "https://api.line.me/v2/bot/chat/loading/start"
    payload = {
        "chatId": line_user_id,
        "loadingSeconds": 20,
    }
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()

def get_profile(user_id):
    """Get a user's LINE profile."""
    access_token = get_token_stateless()
    endpoint = f"https://api.line.me/v2/bot/profile/{user_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()
