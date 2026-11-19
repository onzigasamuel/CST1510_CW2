
# ==========================================
# 1. IMPORTS
# ==========================================

import requests
import pandas as pd
from pathlib import Path


# ==========================================
# 2. API SETTINGS
# ==========================================

API_URL = "https://disease.sh/v3/covid-19/countries"

RENAME = {
    "country": "country",
    "continent": "continent",
    "cases": "cases",
    "deaths": "deaths",
    "recovered": "recovered",
    "tests": "tests",
    "population": "population",
    "active": "active"
}

KEEP = [
    "country",
    "continent",
    "cases",
    "deaths",
    "recovered",
    "tests",
    "population",
    "active"
]

MUST_HAVE = ["cases", "continent"]

RAW_FILE = Path("DATA/raw.csv")


# ==========================================
# 3. GET DATA FROM API
# ==========================================

def get_data():
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print("Error fetching data:", error)
        return None


# ==========================================
# 4. CONVERT DATA INTO A DATAFRAME
# ==========================================

def make_table(records):
    df = pd.json_normalize(records)
    return df


# ==========================================
# 5. CLEAN THE DATA
# ==========================================

def tidy_data(df):
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)

    return df


# ==========================================
# 6. SAVE DATA AS CSV
# ==========================================

def save_data(df):
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_FILE, index=False)

    print("Data saved to:", RAW_FILE)


# ==========================================
# 7. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    data = get_data()

    if data is not None:

        df = make_table(data)

        df = tidy_data(df)

        print(df.head())
        print("Data shape:", df.shape)

        save_data(df)
