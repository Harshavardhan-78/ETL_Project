import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import os
import glob

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = BASE_DIR / "Data" / "raw"
DATA_STAGED_DIR = BASE_DIR / "Data" / "Staged"   # <-- ADD THIS

def get_latest_raw_file():
    raw_files = list(DATA_RAW_DIR.glob("*.json"))
    if not raw_files:
        raise FileNotFoundError("No raw NASA JSON files found!")
    return max(raw_files, key=os.path.getmtime)

def transform_nasa_data():
    latest_file = get_latest_raw_file()
    print(f"Transforming file: {latest_file}")
    
    # Load JSON data
    with open(latest_file, "r") as f:
        data = json.load(f)
    
    # Extract required fields (based on your table)
    transformed = {
        "date": data.get("date"),
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "media_type": data.get("media_type"),
        "image_url": data.get("url") if data.get("media_type") == "image" else None,
        "inserted_at": datetime.now()
    }
    
    # Convert to DataFrame (1 row)
    df = pd.DataFrame([transformed])
    
    # Save to staged csv
    out_path = DATA_STAGED_DIR / "nasa_apod_staged.csv"
    df.to_csv(out_path, index=False)
    print(f"Transformed data saved to: {out_path}")
    return df

if __name__ == "__main__":
    transform_nasa_data()