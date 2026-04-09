import pandas as pd
import os

OUTPUT_PATH = "data/processed/github_repos.csv"

def transform_data(items):
    records = []

    for item in items:
        record = {
            "full_name": item.get("full_name"),
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language", "Unknown"),
            "url": item.get("html_url"),
            "created_at": item.get("created_at")
        }
        records.append(record)

    return pd.DataFrame(records)

def save_to_csv(df):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    if os.path.exists(OUTPUT_PATH):
        df.to_csv(OUTPUT_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(OUTPUT_PATH, index=False)
