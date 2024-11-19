import requests

class RestyClient:
    def __init__(self):
        self.session = requests.Session()

    def get_request(self, endpoint, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.session.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.content

    def post_form_request(self, endpoint, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.session.post(endpoint, headers=headers, data=data)
        response.raise_for_status()
        return response.content

    def post_json_request(self, endpoint, access_token, payload):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = self.session.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        return response

# Initialize the client
client = RestyClient()
