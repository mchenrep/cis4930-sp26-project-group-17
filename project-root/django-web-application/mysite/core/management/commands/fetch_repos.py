import pandas as pd
import requests
import time
from pathlib import Path
from django.core.management.base import BaseCommand


BASE_URL = "https://api.github.com/search/repositories"

def fetch_repositories(query="basketball", per_page=10, max_pages=5):
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

def transform_to_dataframe(items):
    records = []
    for item in items:
        record = {
            "repo_name": item.get("name", "Unknown"),
            "username": item.get("owner", {}).get("login", "Unknown"),
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language", "Unknown"),
            "repo_url": item.get("html_url", "Unknown"),
            "date_created": item.get("created_at", "Unknown")
        }
        records.append(record)
    return pd.DataFrame(records)

def save_dataframe(df, output_file="repos.csv"):
    # Path to the core/ directory
    core_dir = Path(__file__).resolve().parents[2]

    # Path to core/data/
    data_dir = core_dir / "data"
    data_dir.mkdir(exist_ok=True)  # create if missing

    # Final file path
    full_path = data_dir / output_file

    df.to_csv(full_path, index=False)

class Command(BaseCommand):
    help = "Fetch GitHub repos and save to core/data/repos.csv"

    def handle(self, *args, **options):
        items = fetch_repositories()
        df = transform_to_dataframe(items)
        save_dataframe(df)
        self.stdout.write(self.style.SUCCESS(f"Saved {len(df)} rows to core/data/repos.csv"))
