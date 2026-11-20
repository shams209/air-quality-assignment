# Name: Shams ur Rehman
# Roll Number: TRN-2026-000943
# Date: 2026-11-20

import pandas as pd

def check_no_missing_values(df: pd.DataFrame) -> None:
    """
    Checks if there are any remaining missing values. Raises an error if found.
    """
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        raise ValueError(f"Validation Failed: Found {missing_count} missing values!")

def validate_aqi_range(df: pd.DataFrame) -> None:
    """
    Checks if AQI values are between 0 and 500. Raises an error if outside range.
    """
    if 'AQI' in df.columns:
        invalid_aqi = df[(df['AQI'] < 0) | (df['AQI'] > 500)]
        if not invalid_aqi.empty:
            raise ValueError(f"Validation Failed: Found {len(invalid_aqi)} rows with AQI outside 0-500.")