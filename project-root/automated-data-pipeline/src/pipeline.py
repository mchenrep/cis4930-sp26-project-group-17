import requests

BASE_URL = "https://api.balldontlie.io/v1/games"

headers = {
    # Contains free API key for balldontlie API
    "Authorization" : "0b826851-a8df-49d2-88c3-7f70ed8c18b9"
}

response = requests.get(BASE_URL, headers=headers, params={"per_page": 25}, timeout=10)
# Test
data = response.json()
print(data)