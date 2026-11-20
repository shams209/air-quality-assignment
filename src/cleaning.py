# Name: Shams ur Rehman
# Roll Number: TRN-2026-000943
# Date: 2026-11-20

import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes exact duplicate rows from the dataframe.
    """
    df_clean = df.copy()
    return df_clean.drop_duplicates()

def fix_date_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'Date' column from string to datetime format.
    """
    df_clean = df.copy()
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    return df_clean

def fill_missing_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing numeric values with the median of their respective column.
    """
    df_clean = df.copy()
    # Select only numeric columns
    numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_cols:
        median_value = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_value)
        
    return df_clean