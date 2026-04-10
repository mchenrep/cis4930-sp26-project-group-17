import os
import logging
import pandas as pd
import argparse
import api_client

# Make sure folders exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

def transform_to_dataframe(items):
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
    return pd.DataFrame(records)

def save_dataframe(df, output_file="data/processed/github_basketball_repos.csv"):
    df.to_csv(output_file, index=False)
    logging.info(f"Saved {len(df)} rows to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub repositories.")
    parser.add_argument("--query", type=str, default="basketball", help="Search term")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages")
    args = parser.parse_args()

    logging.info(f"Starting pipeline for '{args.query}'...")

    # Call the api_client
    items = api_client.fetch_repositories(query=args.query, per_page=10, max_pages=args.pages)

    if not items:
        logging.warning("No repository data was collected.")
        return

    df = transform_to_dataframe(items)
    
    print(df.head())
    print(f"\nTotal rows collected: {len(df)}")
    
    save_dataframe(df)

if __name__ == "__main__":
    main()