import requests
import time

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

        max_retries = 1
        success = False
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(BASE_URL, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                items = data.get("items", [])

                if not items:
                    break

                all_items.extend(items)
                page += 1
                success = True
                break # Break out of the retry loop if successful

            except requests.exceptions.Timeout:
                print(f"Request timed out on page {page} (Attempt {attempt + 1}/{max_retries + 1})")
                if attempt < max_retries:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)

            except requests.exceptions.RequestException as e:
                print("Request error:", e)
                break 

        if not success:
            print(f"Skipping page due to repeated errors.")
            break

    return all_items