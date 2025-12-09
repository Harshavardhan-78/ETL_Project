import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv


# -----------------------------------------
# Supabase Client
# -----------------------------------------
def get_supabase_client():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

    return create_client(url, key)


# -----------------------------------------
# Check Table Exists
# -----------------------------------------
def check_table_exists(table_name="titanic_data"):
    supabase = get_supabase_client()
    try:
        supabase.table(table_name).select("*").limit(1).execute()
        print(f"Table '{table_name}' exists.")
    except Exception as e:
        print(f"❌ Table '{table_name}' does NOT exist.")
        print("Create it using the SQL you have for titanic_data.")
        print(e)
        exit(1)


# -----------------------------------------
# Load Titanic CSV into Supabase
# -----------------------------------------
def load_titanic_to_supabase(staged_path: str, table_name: str = "titanic_data"):

    # Fix file path
    if not os.path.isabs(staged_path):
        staged_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), staged_path)
        )

    print(f"Looking for file: {staged_path}")

    if not os.path.exists(staged_path):
        print("❌ Titanic CSV not found.")
        return

    supabase = get_supabase_client()
    df = pd.read_csv(staged_path)

    # ALLOWED COLUMNS – we will NOT send embarked_C/Q/S to avoid schema error
    allowed_cols = [
        "survived", "pclass", "sex", "age", "sibsp", "parch", "fare",
        "embarked", "class", "who", "adult_male", "deck", "embark_town",
        "alive", "alone", "family_size", "is_alone", "is_child",
        "age_bin", "fare_per_person", "fare_bin",
        "sex_male", "sex_female",
        # "embarked_C", "embarked_Q", "embarked_S",   # <--- intentionally excluded
    ]

    # keep only columns that exist in df and are allowed
    cols_to_use = [c for c in allowed_cols if c in df.columns]
    df = df[cols_to_use]

    # Convert boolean-like columns
    for col in ["adult_male", "alone", "is_alone", "is_child"]:
        if col in df.columns:
            df[col] = df[col].map({
                True: 1, False: 0,
                "True": 1, "False": 0,
                "true": 1, "false": 0,
            })

    total_rows = len(df)
    batch_size = 50
    print(f"Loading {total_rows} rows to '{table_name}' with columns: {cols_to_use}")

    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i + batch_size].copy()
        batch = batch.where(pd.notnull(batch), None)
        try:
            supabase.table(table_name).insert(batch.to_dict("records")).execute()
            print(f"Inserted {i+1} to {min(i+batch_size, total_rows)}")
        except Exception as e:
            print(f"❌ Batch {i//batch_size + 1} failed: {e}")

    print("✅ Titanic upload completed.")


# -----------------------------------------
# Main
# -----------------------------------------
if __name__ == "__main__":
    csv_path = os.path.join("..", "data", "staged", "titanic_transformed.csv")
    check_table_exists("titanic_data")
    load_titanic_to_supabase(csv_path)
