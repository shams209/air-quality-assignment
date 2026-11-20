# Name: Shams ur Rehman
# Roll Number:  TRN-2026-000943
# Date: 2026-11-20

import pandas as pd
from cleaning import remove_duplicates, fix_date_type, fill_missing_numeric
from validation import check_no_missing_values, validate_aqi_range

print("Loading raw data...")
df = pd.read_csv('../data/raw/air_quality_dataset.csv')
print(f"Original shape: {df.shape}")

print("Cleaning data...")
df = remove_duplicates(df)
df = fix_date_type(df)
df = fill_missing_numeric(df)

print("Validating clean data...")
check_no_missing_values(df)
validate_aqi_range(df)
print("Validation passed!")

print("Saving cleaned data...")
df.to_csv('../data/cleaned/air_quality_cleaned.csv', index=False)
print(f"Cleaned shape: {df.shape}")
print("Pipeline complete. File saved to data/cleaned/")