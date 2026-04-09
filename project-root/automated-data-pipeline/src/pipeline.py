import os
import logging
import requests
import pandas as pd

# Make sure folders exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

BASE_URL = "https://api.github.com/search/repositories"


def fetch_repositories(query="basketball", per_page=10, max_pages=5):
    """
    Fetch repositories from GitHub Search API across multiple pages.
    Returns a list of repository items.
    """
    all_items = []

    for page in range(1, max_pages + 1):
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
                logging.info(f"No more results found on page {page}. Stopping pagination.")
                break

            all_items.extend(items)
            logging.info(f"Fetched {len(items)} items from page {page}.")

        except requests.exceptions.Timeout:
            logging.exception(f"Request timed out on page {page}.")
            break
        except requests.exceptions.RequestException as e:
            logging.exception(f"Request error on page {page}: {e}")
            break

    return all_items


def transform_to_dataframe(items):
    """
    Transform raw GitHub API items into a clean pandas DataFrame.
    """
    records = []

    for item in items:
        record = {
            "repo_name": item.get("name", "Unknown"),
            "full_name": item.get("full_name", "Unknown"),
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language", "Unknown"),
            "username": item.get("owner", {}).get("login", "Unknown"),
            "date_created": item.get("created_at", "Unknown"),
            "open_issues": item.get("open_issues_count", 0),
            "repo_url": item.get("html_url", "Unknown")
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df


def save_dataframe(df, output_file="data/processed/github_basketball_repos.csv"):
    """
    Save DataFrame to CSV.
    """
    df.to_csv(output_file, index=False)
    logging.info(f"Saved {len(df)} rows to {output_file}.")


def main():
    items = fetch_repositories(query="basketball", per_page=10, max_pages=5)

    if not items:
        logging.warning("No repository data was collected.")
        print("No data collected.")
        return

    df = transform_to_dataframe(items)

    print(df.head())
    print(f"\nTotal rows collected: {len(df)}")

    save_dataframe(df)


if __name__ == "__main__":
    main()
