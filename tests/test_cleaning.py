# Name: Shams ur Rehman
# Roll Number: TRN-2026-000943
# Date: 2026-11-18

import pandas as pd
import pytest
from src.cleaning import remove_duplicates, fill_missing_numeric
from src.validation import validate_aqi_range

def test_remove_duplicates():
    df = pd.DataFrame({'City': ['A', 'B', 'A'], 'AQI': [100, 200, 100]})
    result = remove_duplicates(df)
    assert len(result) == 2

def test_fill_missing_numeric():
    df = pd.DataFrame({'AQI': [50.0, 60.0, None, 70.0]})
    result = fill_missing_numeric(df)
    # Median of 50, 60, 70 is 60. None should become 60.0
    assert result['AQI'].isnull().sum() == 0
    assert result['AQI'][2] == 60.0

def test_validate_aqi_range_fails():
    df = pd.DataFrame({'AQI': [50, 600, 70]})
    with pytest.raises(ValueError):
        validate_aqi_range(df)