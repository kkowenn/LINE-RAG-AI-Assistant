import requests

def post_form_request(endpoint, data):
    response = requests.post(endpoint, data=data)
    response.raise_for_status()
    return response.json()

def post_json_request(endpoint, token, payload):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    return response
