# Load.py
import os
import time
from pathlib import Path

import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure the DataFrame has column names that match the DB table:
    (date, title, explanation, media_type, image_url, inserted_at)

    Accept common variants and normalize them to the expected names.
    """
    col_map = {}

    # common alternatives -> canonical
    alt_map = {
        "url": "image_url",
        "image": "image_url",
        "imageUrl": "image_url",
        "img_url": "image_url",
        "datetime": "inserted_at",
        "created_at": "inserted_at",
        "time": "inserted_at",
        "media": "media_type",
    }

    for col in df.columns:
        lower = col.lower()
        if lower in alt_map:
            col_map[col] = alt_map[lower]
        else:
            # if it already matches one of expected names (case-insensitive), map to canonical
            if lower == "date":
                col_map[col] = "date"
            elif lower == "title":
                col_map[col] = "title"
            elif lower == "explanation":
                col_map[col] = "explanation"
            elif lower == "media_type":
                col_map[col] = "media_type"
            elif lower == "image_url":
                col_map[col] = "image_url"
            elif lower == "inserted_at":
                col_map[col] = "inserted_at"
            # otherwise leave as-is (will be caught as missing later)

    if col_map:
        df = df.rename(columns=col_map)

    return df


def load_nasa_to_supabase(batch_size: int = 100, pause_between_batches: float = 0.3):
    # Build a robust absolute path relative to this script:
    BASE_DIR = Path(__file__).resolve().parent.parent  # ETL_NASA/
    csv_path = BASE_DIR / "Data" / "Staged" / "nasa_apod_staged.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")

    df = pd.read_csv(csv_path)

    # Normalize common alternative column names
    df = normalize_columns(df)

    # Required (canonical) columns that must match the DB table
    required_cols = {"date", "title", "explanation", "media_type", "image_url", "inserted_at"}
    missing = required_cols - set(df.columns)
    if missing:
        # If some required columns are missing but can be created, attempt that:
        # - If explanation/title missing, fail (these are NOT nullable per your DDL).
        # - For image_url/media_type, we can safely fill with None.
        fail_cols = {"date", "title", "explanation", "inserted_at"}
        if fail_cols & missing:
            raise ValueError(f"Staged CSV is missing required columns: {missing}")
        # fill optional missing columns with None
        for c in missing:
            df[c] = None

    # Convert/format date & inserted_at
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")

    # If any date parsing failed, notify
    if df["date"].isnull().any():
        raise ValueError("One or more 'date' values could not be parsed into YYYY-MM-DD.")

    # Replace NaN with None so Supabase inserts NULLs
    df = df.where(pd.notnull(df), None)

    total = len(df)
    if total == 0:
        print("No rows to load. Exiting.")
        return

    for i in range(0, total, batch_size):
        batch = df.iloc[i : i + batch_size].to_dict("records")
        try:
            res = supabase.table("nasa_apod").insert(batch).execute()
            # basic success print - res shape may vary by supabase client version
            print(f"Inserted rows {i+1} → {min(i + batch_size, total)}")
        except Exception as e:
            # Print error and include batch index range for easier debugging
            print(f"[ERROR] Inserting rows {i+1} → {min(i + batch_size, total)}: {e}")
            # Decide whether to continue or raise — here we continue to allow partial loads
            # If you want to stop on first error, replace the next line with `raise`
        time.sleep(pause_between_batches)

    print("Finished loading NASA data.")


if __name__ == "__main__":
    load_nasa_to_supabase()
