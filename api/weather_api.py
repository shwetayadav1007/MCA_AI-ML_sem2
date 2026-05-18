import requests

BASE_URL = 'https://api.open-meteo.com/v1/forecast'


def fetch_weather_data(latitude: str, longitude: str, params=None):
    query = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,relativehumidity_2m,precipitation',
        'daily': 'rain_sum,temperature_2m_max,temperature_2m_min',
        'timezone': 'auto',
    }
    if params:
        query.update(params)

    response = requests.get(BASE_URL, params=query, timeout=15)
    response.raise_for_status()
    payload = response.json()
    return {
        'location': {'latitude': latitude, 'longitude': longitude},
        'hourly': payload.get('hourly', {}),
        'daily': payload.get('daily', {}),
    }
