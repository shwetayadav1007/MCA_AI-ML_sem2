import os
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
try:
    from backend.preprocess import preprocess
    from backend.model_utils import create_prediction_response
    from backend.db import log_alert
except ImportError:
    from preprocess import preprocess
    from model_utils import create_prediction_response
    from db import log_alert
from api.weather_api import fetch_weather_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / 'models' / 'groundwater_model.pkl'
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'groundwater.csv'
PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed' / 'cleaned_groundwater.csv'
FEATURES = ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage', 'Season']
SEASON_MAP = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Monsoon': 3}

app = Flask(__name__)
CORS(app)


def encode_season(value):
    if isinstance(value, str):
        return SEASON_MAP.get(value.title(), 0)
    return int(value)


def load_model():
    if not MODEL_PATH.exists():
        print('Trained model not found. Running training...')
        try:
            from backend.train_model import train_model
        except ImportError:
            from train_model import train_model
        train_model()
    return joblib.load(MODEL_PATH)

model = load_model()


@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'Dataset file is required.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    df = pd.read_csv(file)
    df.to_csv(DATA_PATH, index=False)
    preprocess()

    return jsonify({'status': 'Dataset uploaded and preprocessed successfully.'})


@app.route('/train-model', methods=['POST'])
def train_model_endpoint():
    try:
        from backend.train_model import train_model
    except ImportError:
        from train_model import train_model
    metrics = train_model()
    return jsonify({'status': 'Model trained successfully.', 'metrics': metrics})


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({'error': 'JSON payload required.'}), 400

    missing = [feature for feature in FEATURES if feature not in payload]
    if missing:
        return jsonify({'error': 'Missing required fields.', 'missing': missing}), 400

    try:
        values = []
        for feature in FEATURES:
            value = payload[feature]
            if feature == 'Season':
                value = encode_season(value)
            values.append(float(value))
    except (ValueError, TypeError):
        return jsonify({'error': 'Inputs must be numeric or valid season name.'}), 400

    prediction = model.predict([values])[0]
    response = create_prediction_response(prediction)
    if response['risk_category'] != 'Safe':
        alert = {
            'message': f"Groundwater risk {response['risk_category']} detected.",
            'risk': response['risk_category'],
            'created_at': datetime.utcnow(),
        }
        try:
            log_alert(alert)
        except Exception:
            pass

    return jsonify(response)


@app.route('/weather-data', methods=['GET'])
def weather_data():
    latitude = request.args.get('lat', default='22.57')
    longitude = request.args.get('lon', default='88.36')
    try:
        weather = fetch_weather_data(latitude, longitude)
        return jsonify({'status': 'ok', 'weather': weather})
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


@app.route('/alerts', methods=['GET'])
def alerts():
    try:
        try:
            from backend.db import fetch_alerts
        except ImportError:
            from db import fetch_alerts
        active_alerts = fetch_alerts(limit=10)
        for alert in active_alerts:
            alert['_id'] = str(alert['_id'])
        return jsonify({'alerts': active_alerts})
    except Exception:
        return jsonify({'alerts': []})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': MODEL_PATH.name})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
