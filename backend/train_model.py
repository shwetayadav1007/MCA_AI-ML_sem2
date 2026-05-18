from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import joblib
try:
    from backend.preprocess import preprocess
except ImportError:
    from preprocess import preprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEANED_PATH = PROJECT_ROOT / 'data' / 'processed' / 'cleaned_groundwater.csv'
MODEL_PATH = PROJECT_ROOT / 'models' / 'groundwater_model.pkl'
FEATURES = ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage', 'Season']


def train_model():
    if not CLEANED_PATH.exists():
        print('Cleaned dataset not found. Running preprocessing...')
        preprocess()

    print('Loading cleaned dataset from:', CLEANED_PATH)
    df = pd.read_csv(CLEANED_PATH)
    X = df[FEATURES]
    y = df['Groundwater_Level']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        'mae': round(mae, 3),
        'rmse': round(rmse, 3),
        'r2': round(r2, 3),
    }
    print('Model training complete and saved to:', MODEL_PATH)
    print(f"Test MAE: {metrics['mae']}")
    print(f"Test RMSE: {metrics['rmse']}")
    print(f"Test R2: {metrics['r2']}")
    return metrics


if __name__ == '__main__':
    train_model()
