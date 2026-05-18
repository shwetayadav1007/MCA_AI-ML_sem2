import sys
from pathlib import Path
import joblib
from model_utils import create_prediction_response

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / 'models' / 'groundwater_model.pkl'
FEATURES = ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage', 'Season']
SEASON_MAP = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Monsoon': 3}


def encode_season(value):
    if isinstance(value, str):
        return SEASON_MAP.get(value.title(), 0)
    return int(value)

if not MODEL_PATH.exists():
    raise FileNotFoundError('Model not found. Run python backend/train_model.py first.')

model = joblib.load(MODEL_PATH)

if len(sys.argv) == len(FEATURES) + 1:
    raw_values = sys.argv[1:]
    values = []
    for name, raw in zip(FEATURES, raw_values):
        if name == 'Season':
            values.append(encode_season(raw))
        else:
            values.append(float(raw))
else:
    print('Usage: python backend/predict.py <Rainfall> <Temperature> <Humidity> <Soil_Moisture> <Water_Usage> <Season>')
    print('Using sample values for demonstration.')
    values = [120.0, 30.0, 70.0, 35.0, 210.0, 2.0]

prediction = model.predict([values])[0]
response = create_prediction_response(prediction)

print('Input features:')
for name, value in zip(FEATURES, values):
    print(f' - {name}: {value}')
print(f"Predicted groundwater level: {response['groundwater_level']}")
print(f"Risk category: {response['risk_category']}")
print(f"Recommendation: {response['recommendation']}")
