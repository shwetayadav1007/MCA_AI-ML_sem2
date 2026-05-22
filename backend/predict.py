import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Union

def load_models(models_dir):
    """
    Load the trained Linear Regression and XGBoost models.
    """
    lr_model_path = os.path.join(models_dir, 'linear_regression_model.pkl')
    xgb_model_path = os.path.join(models_dir, 'xgboost_model.pkl')
    
    if not os.path.exists(lr_model_path) or not os.path.exists(xgb_model_path):
        raise FileNotFoundError("Model files not found. Please train the models first.")
    
    lr_model = joblib.load(lr_model_path)
    xgb_model = joblib.load(xgb_model_path)
    
    return lr_model, xgb_model

def preprocess_input(input_data: Dict) -> np.ndarray:
    """
    Preprocess input data for prediction.
    Expected input keys: Rainfall, Temperature, Humidity, Water_Usage, Soil_Moisture, Season
    """
    # Create a DataFrame from input data
    df = pd.DataFrame([input_data])
    
    # Handle Season encoding (one-hot encoding)
    # We need to create the same columns as during training
    season = df['Season'][0]
    season_dummies = pd.get_dummies(df['Season'], prefix='Season')
    
    # Drop the original Season column
    df = df.drop('Season', axis=1)
    
    # Concatenate with the original dataframe
    df = pd.concat([df, season_dummies], axis=1)
    
    # Ensure all expected season columns are present (Spring, Summer, Winter)
    # This handles cases where a particular season might not be in the input
    expected_seasons = ['Season_Spring', 'Season_Summer', 'Season_Winter']
    for season_col in expected_seasons:
        if season_col not in df.columns:
            df[season_col] = 0
    
    # Reorder columns to match training order (important for model prediction)
    # We'll define the expected column order based on what was used in training
    # Since we don't have the exact column order saved, we'll assume a logical order
    # In a production system, you'd save the column order with the model
    
    # For now, let's create a consistent order
    base_features = ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage']
    season_features = ['Season_Spring', 'Season_Summer', 'Season_Winter']
    expected_columns = base_features + season_features
    
    # Ensure we have all expected columns
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder columns
    df = df[expected_columns]
    
    return df.values

def predict_groundwater_level(input_data: Dict, models_dir=None) -> Dict:
    """
    Predict groundwater level and risk category.
    
    Args:
        input_data: Dictionary containing Rainfall, Temperature, Humidity, 
                   Water_Usage, Soil_Moisture, Season
        models_dir: Directory containing the trained models (optional)
    
    Returns:
        Dictionary with prediction results
    """
    if models_dir is None:
        models_dir = os.path.join('..', 'models')
    
    # Load models
    lr_model, xgb_model = load_models(models_dir)
    
    # Preprocess input
    processed_input = preprocess_input(input_data)
    
    # Make predictions
    lr_prediction = lr_model.predict(processed_input)[0]
    xgb_prediction = xgb_model.predict(processed_input)[0]
    
    # For final prediction, we'll use the better performing model (XGBoost typically)
    # Or we could average them, but let's use XGBoost as it's usually more accurate
    final_prediction = xgb_prediction
    
    # Determine risk category
    risk_category = groundwater_risk_category(final_prediction)
    
    # Prepare result
    result = {
        'groundwater_level_prediction': round(final_prediction, 2),
        'linear_regression_prediction': round(lr_prediction, 2),
        'xgboost_prediction': round(xgb_prediction, 2),
        'risk_category': risk_category,
        'input_parameters': input_data
    }
    
    return result

def groundwater_risk_category(level: float) -> str:
    """
    Categorize groundwater level into risk categories.
    """
    if level > 50:  # Safe threshold (example)
        return "Safe"
    elif level > 30:  # Moderate threshold
        return "Moderate"
    else:
        return "Critical"

# Example usage function
def example_prediction():
    """
    Example of how to use the prediction function.
    """
    # Example input
    example_input = {
        'Rainfall': 100,
        'Temperature': 28,
        'Humidity': 70,
        'Water_Usage': 250,
        'Soil_Moisture': 35,
        'Season': 'Summer'
    }
    
    try:
        result = predict_groundwater_level(example_input)
        print("Prediction Result:")
        print(f"Groundwater Level Prediction: {result['groundwater_level_prediction']}")
        print(f"Risk Category: {result['risk_category']}")
        print(f"Linear Regression Prediction: {result['linear_regression_prediction']}")
        print(f"XGBoost Prediction: {result['xgboost_prediction']}")
        return result
    except Exception as e:
        print(f"Error making prediction: {e}")
        return None

if __name__ == "__main__":
    # Run example prediction
    example_prediction()