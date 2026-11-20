# Name: Shams ur Rehman
# Roll Number: TRN-2026-000943
# Date: 2026-11-20
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Get the absolute path to the project root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("1. Loading cleaned data...")
    clean_path = os.path.join(BASE_DIR, 'data', 'cleaned', 'air_quality_cleaned.csv')
    df = pd.read_csv(clean_path)

    print("2. Framing problem and splitting data...")
    # Drop 'AQI' (target) and 'Date' (to prevent leakage)
    X = df.drop(columns=['AQI', 'Date'])
    y = df['AQI']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"   Training data: {X_train.shape[0]} rows | Testing data: {X_test.shape[0]} rows")

    print("3. Building preprocessing pipeline...")
    numeric_features = ['PM2.5', 'PM10', 'Ozone', 'NO2', 'CO', 'SO2', 'Temperature', 'Humidity']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_features = ['City']
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    print("4. Training models...")
    models = {
        'Baseline (Dummy)': DummyRegressor(strategy='mean'),
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(random_state=42)
    }

    results = []
    best_model = None
    best_r2 = -float('inf')

    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results.append({'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2})
        print(f"   --- {name} ---")
        print(f"   MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.2f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model = pipeline

    print("\n5. Saving Results...")
    report_path = os.path.join(BASE_DIR, 'outputs', 'reports', 'model_comparison.csv')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    results_df = pd.DataFrame(results)
    results_df.to_csv(report_path, index=False)
    print(f"   Saved table to: {report_path}")

    print("\n6. Saving the best model...")
    model_path = os.path.join(BASE_DIR, 'models', 'aqi_model.joblib')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model, model_path)
    print(f"   Saved model to: {model_path}")
    print("\nPipeline complete! You have finished Part B.")

if __name__ == "__main__":
    main()