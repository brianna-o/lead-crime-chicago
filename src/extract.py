import time
import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://data.cityofchicago.org/resource"
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PAGE_SIZE = 50_000

def get_page(dataset_id, params):
    """Request one page of results from a Chicago Data Portal dataset."""
    url = f"{BASE_URL}/{dataset_id}.json"
    response = requests.get(url, params=params, timeout=300)
    response.raise_for_status()
    return response.json()

def fetch_all(dataset_id, params):
    """Download every row of a dataset, one page at a time."""
    all_rows = []
    offset = 0

    while True:
        page_params = {**params, "$limit": PAGE_SIZE, "$offset": offset}
        page = get_page(dataset_id, page_params)
        all_rows.extend(page)
        print(f" {dataset_id}: {len(all_rows):,} rows so far")

        if len(page) < PAGE_SIZE:
            break

        offset += PAGE_SIZE
        time.sleep(1)

    return pd.DataFrame(all_rows)

def save(df, name):
    """Save a DataFrame as a CSV in data/raw/."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {len(df):,} rows x {df.shape[1]} columns to {path.name}\n")

def extract_crimes():
    """Count crimes by year, community area, and crime type on the server."""
    params = {
        "$select": "year, community_area, fbi_code, primary_type, count(*) AS incidents",
        "$where": "year BETWEEN 2001 AND 2025 AND community_area IS NOT NULL",
        "$group": "year, community_area, fbi_code, primary_type",
        "$order": "year, community_area, fbi_code, primary_type",
    }
    return fetch_all("ijzp-q8t2", params)

if __name__ == "__main__":
    lead = fetch_all("v2z5-jyrq", {"$order": "community_area_number"})
    save(lead, "blood_lead")

    socio = fetch_all("kn9c-c2s2", {"$order": "ca"})
    save(socio, "socioeconomic")

    crimes = extract_crimes()
    save(crimes, "crimes_by_area_year")