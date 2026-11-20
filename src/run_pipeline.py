# Name: Shams ur Rehman
# Roll Number:  TRN-2026-000943
# Date: 2026-11-20

import pandas as pd
import os
from cleaning import remove_duplicates, fix_date_type, fill_missing_numeric
from validation import check_no_missing_values, validate_aqi_range

# Get the absolute path to the project root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_pipeline():
    print("1. Loading raw data...")
    raw_path = os.path.join(BASE_DIR, 'data', 'raw', 'air_quality_dataset.csv')
    df = pd.read_csv(raw_path)
    print(f"   Original shape: {df.shape}")

    print("2. Cleaning data...")
    df = remove_duplicates(df)
    df = fix_date_type(df)
    df = fill_missing_numeric(df)
    print("   Cleaning complete.")

    print("3. Validating clean data...")
    check_no_missing_values(df)
    validate_aqi_range(df)
    print("   Validation passed!")

    print("4. Saving cleaned data...")
    clean_path = os.path.join(BASE_DIR, 'data', 'cleaned', 'air_quality_cleaned.csv')
    df.to_csv(clean_path, index=False)
    print(f"   Cleaned shape: {df.shape}")
    print("Pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()