import os
import pandas as pd
from Ex_Titanic import extract_data   # your extractor


def transform_data(raw_path: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staged_dir = os.path.join(base_dir, "data", "staged")
    os.makedirs(staged_dir, exist_ok=True)

    df = pd.read_csv(raw_path)

    # ---------------------------
    # Handle Missing Values
    # ---------------------------
    numeric_cols = ["age", "sibsp", "parch", "fare"]
    cat_cols = ["sex", "embarked", "deck", "embark_town", "class", "who", "alive"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    df["deck"] = df["deck"].fillna("Unknown")

    # ---------------------------
    # Feature Engineering
    # ---------------------------

    df["family_size"] = df["sibsp"] + df["parch"] + 1
    df["is_alone"] = (df["family_size"] == 1).astype(int)
    df["is_child"] = (df["age"] < 16).astype(int)

    df["age_bin"] = pd.cut(
        df["age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["child", "teen", "young_adult", "adult", "senior"],
        include_lowest=True
    )

    df["fare_per_person"] = df["fare"] / df["family_size"]
    df["fare_bin"] = pd.qcut(df["fare"], 4, labels=["low", "mid_low", "mid_high", "high"])

    # one-hot encoding for sex
    df["sex_male"] = (df["sex"] == "male").astype(int)
    df["sex_female"] = (df["sex"] == "female").astype(int)

    # one-hot encoding for embarked
    embarked = pd.get_dummies(df["embarked"], prefix="embarked")
    df = pd.concat([df, embarked], axis=1)

    # ---------------------------
    # Save final transformed CSV
    # ---------------------------
    out_path = os.path.join(staged_dir, "titanic_transformed.csv")
    df.to_csv(out_path, index=False)

    print(f"✅ Titanic transformed CSV saved at: {out_path}")
    return out_path


if __name__ == "__main__":
    raw_path = extract_data()
    transform_data(raw_path)
