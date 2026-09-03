import os
import pandas as pd

def get_latest_json_file(directory="data"):
    """
    Finds the latest trends JSON file matching 'trends_' without using glob.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
        
    # List all files in the directory and filter for trends JSON files
    files = [f for f in os.listdir(directory) if f.startswith("trends_") and f.endswith(".json")]
    
    if not files:
        raise FileNotFoundError(f"No matching JSON files found in '{directory}/' folder.")
    
    # Sort files alphabetically (handles YYYYMMDD order perfectly) and pick the last one
    files.sort()
    latest_file = files[-1]
    
    return os.path.join(directory, latest_file)

def main():
    # ---------------------------------------------------------
    # 1 — Load the JSON File (4 marks)
    # ---------------------------------------------------------
    try:
        # Dynamically find the file from Task 1
        json_file_path = get_latest_json_file("data")
    except FileNotFoundError as e:
        print(e)
        return

    # Load JSON file into a Pandas DataFrame
    df = pd.read_json(json_file_path)
    
    initial_count = len(df)
    print(f"Loaded {initial_count} stories from {json_file_path}\n")

    # ---------------------------------------------------------
    # 2 — Clean the Data (10 marks)
    # ---------------------------------------------------------
    
    # A. Duplicates — remove any rows with the same post_id
    df = df.drop_duplicates(subset=["post_id"])
    print(f"After removing duplicates: {len(df)}")

    # B. Missing values — drop rows where critical fields are missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # C. Data types — force score and num_comments into strict integer values
    # We fill missing comment fields with 0 before conversion to prevent float cast errors
    df["num_comments"] = df["num_comments"].fillna(0).astype('int64')
    df["score"] = df["score"].astype('int64')

    # D. Low quality — filter out stories where score is strictly less than 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}\n")

    # E. Whitespace — strip trailing and leading extra spaces from the title column
    df["title"] = df["title"].astype(str).str.strip()

    # ---------------------------------------------------------
    # 3 — Save as CSV (6 marks)
    # ---------------------------------------------------------
    output_csv_path = os.path.join("data", "trends_clean.csv")
    
    # Save the cleaned DataFrame without the numerical Pandas index column
    df.to_csv(output_csv_path, index=False)
    print(f"Saved {len(df)} rows to {output_csv_path}\n")

    # Group records by category and output a clean summary distribution
    print("Stories per category:")
    category_counts = df["category"].value_counts()
    for category, count in category_counts.items():
        print(f"  {category:<15} {count}")

if __name__ == "__main__":
    main()
