# Name: [Your Name]
# Roll Number:  TRN-2026-000943
# Date: 2026-11-22

import pandas as pd
import joblib
import sys
import os

def predict_new_data(input_csv_path, output_csv_path):
    # Get the absolute path to the project root folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, 'models', 'aqi_model.joblib')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Run train_model.py first.")
    
    print("Loading model pipeline...")
    pipeline = joblib.load(model_path)
    
    print(f"Reading new data from {input_csv_path}...")
    new_data = pd.read_csv(input_csv_path)
    
    # Drop columns that were not used for training
    cols_to_drop = ['Date', 'AQI']
    for col in cols_to_drop:
        if col in new_data.columns:
            new_data = new_data.drop(columns=[col])
            
    print("Generating predictions...")
    predictions = pipeline.predict(new_data)
    
    output_df = pd.read_csv(input_csv_path)
    output_df['Predicted_AQI'] = predictions
    output_df.to_csv(output_csv_path, index=False)
    
    print(f"✅ Predictions saved to {output_csv_path}")
    
    # Feature Importance (Bonus)
    try:
        # Get the actual model from the pipeline (it could be RF or LinearRegression)
        final_model = pipeline.named_steps['model']
        if hasattr(final_model, 'feature_importances_'):
            importances = final_model.feature_importances_
            
            preprocessor = pipeline.named_steps['preprocessor']
            cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
            cat_features = cat_encoder.get_feature_names_out(['City'])
            
            all_features = ['PM2.5', 'PM10', 'Ozone', 'NO2', 'CO', 'SO2', 'Temperature', 'Humidity'] + list(cat_features)
            
            importance_df = pd.DataFrame({'Feature': all_features, 'Importance': importances})
            importance_df = importance_df.sort_values(by='Importance', ascending=False)
            
            print("\n--- Top 5 Most Important Features ---")
            print(importance_df.head(5).to_string(index=False))
            print("\nNote: It makes sense that PM2.5 and PM10 are the most important features for predicting AQI, as they are primary pollutants.")
    except Exception as e:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python predict.py <input_csv> <output_csv>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    predict_new_data(input_file, output_file)