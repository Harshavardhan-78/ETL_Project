#1.
import os
import seaborn as sns
import pandas as pd

#2.
def extract_data():
    # Get base directory (parent of current file)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create raw data directory
    data_dir = os.path.join(base_dir, "Data", "raw")
    os.makedirs(data_dir, exist_ok=True)
    
    # Load dataset
    df = sns.load_dataset("titanic")
    
    # Save raw CSV
    raw_path = os.path.join(data_dir, "Titanic_raw.csv")
    df.to_csv(raw_path, index=False)
    
    print(f"Data extracted and saved at: {raw_path}")
    return raw_path


# Run when executed directly
if __name__ == "__main__":
    extract_data()
