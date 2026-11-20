# Data Quality Report

## 1. Executive Summary
This report documents the data cleaning and validation pipeline applied to the raw `air_quality_dataset.csv`. The goal was to handle missing values, remove duplicates, and handle extreme outliers so the dataset is ready for Exploratory Data Analysis (EDA) and Machine Learning.

## 2. Data Quality Metrics (Before vs. After)

| Metric | Before Cleaning | After Cleaning | Action Taken |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 5583 | 5583 | Removed 0 duplicates *(Update this if your code finds duplicates)* |
| **AQI Missing Values** | 111 | 0 | Filled with Median |
| **PM2.5 Missing Values** | 97 | 0 | Filled with Median |
| **PM10 Missing Values** | 60 | 0 | Filled with Median |
| **Ozone Missing Values** | 75 | 0 | Filled with Median |
| **NO2 Missing Values** | 93 | 0 | Filled with Median |
| **CO Missing Values** | 162 | 0 | Filled with Median |
| **SO2 Missing Values** | 129 | 0 | Filled with Median |
| **Temperature Missing**| 148 | 0 | Filled with Median |
| **Humidity Missing** | 104 | 0 | Filled with Median |

## 3. Validation Pass Rate
- The dataset was run through validation scripts (`src/validation.py`).
- **Pass Rate:** 100% of the rows passed the AQI range check (0-500) and Temperature range check.

## 4. Cleaning Steps Performed
1.  **Duplicates:** Checked for duplicate rows across all columns. *(Note: If you ran `df.drop_duplicates()`, mention how many rows were dropped here. If 0, say "No exact duplicates were found").*
2.  **Missing Values:** All numerical columns with missing values (AQI, PM2.5, etc.) were imputed using the **Median**.
3.  **Feature Engineering:** Added `Temp_F` (converted temperature to Fahrenheit) and `PM_Ratio` (calculated the ratio between PM2.5 and PM10).