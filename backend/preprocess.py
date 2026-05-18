from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / 'data' / 'raw' / 'groundwater.csv'
PROCESSED_PATH = PROJECT_ROOT / 'data' / 'processed' / 'cleaned_groundwater.csv'
REQUIRED_COLUMNS = [
    'Rainfall',
    'Temperature',
    'Humidity',
    'Soil_Moisture',
    'Water_Usage',
    'Season',
    'Groundwater_Level',
]


def load_raw_data():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f'Raw dataset not found. Place groundwater.csv in {RAW_PATH.parent}')

    df = pd.read_csv(RAW_PATH)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError('Dataset is missing required columns: ' + ', '.join(missing))

    return df


def encode_season(df: pd.DataFrame) -> pd.DataFrame:
    season_map = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Monsoon': 3}
    df['Season'] = df['Season'].astype(str).map(season_map).fillna(0).astype(int)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df = df[REQUIRED_COLUMNS].copy()
    for col in ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage', 'Groundwater_Level']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = encode_season(df)
    df.fillna(df.mean(numeric_only=True), inplace=True)
    return df


def save_cleaned_data(df: pd.DataFrame):
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print('Saved cleaned dataset to:', PROCESSED_PATH)


def preprocess():
    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)
    save_cleaned_data(cleaned_df)
    return cleaned_df


if __name__ == '__main__':
    preprocess()
