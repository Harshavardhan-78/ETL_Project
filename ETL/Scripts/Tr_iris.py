import os
import pandas as pd
from Ex_iris import extract_data


def transform_data(raw_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Use the same "Data" capitalization as in Ex_iris
    staged_dir = os.path.join(base_dir, "Data", "staged")
    os.makedirs(staged_dir, exist_ok=True)

    # Read raw data
    df = pd.read_csv(raw_path)

    # 1. Handle missing values
    numerical_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())

    df["species"] = df["species"].fillna(df["species"].mode()[0])

    # 2. Feature engineering
    df["sepal_ratio"] = df["sepal_length"] / df["sepal_width"]
    df["petal_ratio"] = df["petal_length"] / df["petal_width"]
    df["is_petal_long"] = (df["petal_length"] > df["petal_length"].median()).astype(int)

    # 3. Drop unnecessary columns (currently nothing to drop)
    # If you want to drop later, put column names in this list.
    df.drop(columns=[], inplace=True, errors="ignore")

    # 4. Save transformed data
    staged_path = os.path.join(staged_dir, "iris_transformed.csv")
    df.to_csv(staged_path, index=False)
    print(f"Data transformed and saved at: {staged_path}")
    return staged_path


if __name__ == "__main__":
    raw_path = extract_data()
    transform_data(raw_path)
