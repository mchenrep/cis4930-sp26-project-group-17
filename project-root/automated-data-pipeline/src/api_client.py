import requests

BASE_URL = "https://api.github.com/search/repositories"

def fetch_repositories(query="python education", per_page=10, max_pages=3):
    all_items = []
    page = 1

    while page <= max_pages:
        params = {
            "q": query,
            "per_page": per_page,
            "page": page
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            if not items:
                break

            all_items.extend(items)
            page += 1

        except requests.exceptions.Timeout:
            print("Request timed out. Skipping page:", page)
            break

        except requests.exceptions.RequestException as e:
            print("Request error:", e)
            break

    return all_items
