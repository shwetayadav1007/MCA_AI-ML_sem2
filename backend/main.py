from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'groundwater.csv'

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f'Dataset not found. Place groundwater.csv in {DATA_PATH.parent}\n'
        'Ensure the dataset includes Date, Region, Rainfall, Temperature, Humidity, Soil_Moisture, Water_Usage, Season, and Groundwater_Level.'
    )

print('Loading dataset from:', DATA_PATH)
df = pd.read_csv(DATA_PATH)

print('\nRows:', len(df))
print('\nData sample:')
print(df.head())

print('\nDataset info:')
print(df.info())

print('\nDescriptive statistics:')
print(df.describe())

print('\nMissing values by column:')
print(df.isnull().sum())
