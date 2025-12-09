import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv


# -----------------------------------------
# Initialize Supabase Client
# -----------------------------------------
def get_supabase_client():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

    return create_client(url, key)


# -----------------------------------------
# Verify table exists first (no RPC)
# -----------------------------------------
def check_table_exists(table_name="iris_data"):
    supabase = get_supabase_client()
    try:
        supabase.table(table_name).select("*").limit(1).execute()
        print(f"Table '{table_name}' exists.")
    except Exception as e:
        print(f"❌ Table '{table_name}' does NOT exist.")
        print("Please create it manually using this SQL:\n")
        print("""
CREATE TABLE iris_data (
    id BIGSERIAL PRIMARY KEY,
    sepal_length FLOAT,
    sepal_width FLOAT,
    petal_length FLOAT,
    petal_width FLOAT,
    species TEXT,
    sepal_ratio FLOAT,
    petal_ratio FLOAT,
    is_petal_long INTEGER
);
""")
        exit(1)


# -----------------------------------------
# Load CSV into Supabase
# -----------------------------------------
def load_to_supabase(staged_path: str, table_name: str = "iris_data"):

    if not os.path.isabs(staged_path):
        staged_path = os.path.abspath(os.path.join(os.path.dirname(__file__), staged_path))

    print(f"Looking for the data file at: {staged_path}")

    if not os.path.exists(staged_path):
        print(f"❌ Error: File not found at {staged_path}")
        print("Run transform_iris.py first.")
        return

    supabase = get_supabase_client()
    df = pd.read_csv(staged_path)
    total_rows = len(df)
    batch_size = 50

    # Convert boolean-like column to integers
    if "is_petal_long" in df.columns:
        df["is_petal_long"] = df["is_petal_long"].map({True: 1, False: 0, "true": 1, "false": 0})

    print(f"Loading {total_rows} rows into '{table_name}'...")

    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i + batch_size].copy()
        batch = batch.where(pd.notnull(batch), None)
        records = batch.to_dict("records")

        try:
            supabase.table(table_name).insert(records).execute()
            end = min(i + batch_size, total_rows)
            print(f"Inserted rows {i+1} – {end}")
        except Exception as e:
            print(f"❌ Batch {i//batch_size + 1} failed: {e}")

    print("✅ Upload completed.")


# -----------------------------------------
# Main Execution
# -----------------------------------------
if __name__ == "__main__":
    staged_csv_path = os.path.join("..", "data", "staged", "iris_transformed.csv")

    check_table_exists("iris_data")
    load_to_supabase(staged_csv_path)
