from flask import Flask, request, jsonify
import os
import sys
import pandas as pd
import numpy as np

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from train_model import main as train_main
from predict import predict_groundwater_level, groundwater_risk_category

app = Flask(__name__)

@app.route('/train-model', methods=['POST'])
def train_model():
    """
    Endpoint to trigger model training.
    """
    try:
        # We'll call the main function from train_model.py
        # Note: In a production setting, you might want to run this as a background task
        # For simplicity, we are running it synchronously.
        train_main()
        return jsonify({
            'message': 'Model training completed successfully.',
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Error during model training: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make a prediction based on input features.
    Expected JSON input:
    {
        "Rainfall": float,
        "Temperature": float,
        "Humidity": float,
        "Water_Usage": float,
        "Soil_Moisture": float,
        "Season": string (one of 'Spring', 'Summer', 'Winter')
    }
    """
    try:
        # Get JSON data from request
        input_data = request.get_json()
        
        # Validate input
        required_keys = ['Rainfall', 'Temperature', 'Humidity', 'Water_Usage', 'Soil_Moisture', 'Season']
        for key in required_keys:
            if key not in input_data:
                return jsonify({
                    'message': f'Missing required key: {key}',
                    'status': 'error'
                }), 400
        
        # Make prediction
        result = predict_groundwater_level(input_data)
        
        return jsonify({
            'prediction': result['groundwater_level_prediction'],
            'risk_category': result['risk_category'],
            'linear_regression_prediction': result['linear_regression_prediction'],
            'xgboost_prediction': result['xgboost_prediction'],
            'input_parameters': result['input_parameters'],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Error during prediction: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)