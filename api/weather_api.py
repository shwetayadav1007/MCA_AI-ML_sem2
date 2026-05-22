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


def fetch_current_weather(latitude: str, longitude: str):
    """Fetch a simplified current weather object (temperature, humidity, rainfall, weather).

    Uses Open-Meteo `current_weather` and `hourly` payloads to extract humidity
    and precipitation for the current hour.
    Returns a dict with keys: temperature, humidity, rainfall, weather
    """
    query = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': 'true',
        'hourly': 'temperature_2m,relativehumidity_2m,precipitation',
        'timezone': 'auto',
    }
    resp = requests.get(BASE_URL, params=query, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    # default empty values
    temperature = None
    humidity = None
    rainfall = 0.0
    weather = 'Unknown'

    # current_weather contains immediate temperature and time
    current = payload.get('current_weather') or {}
    if current:
        temperature = current.get('temperature')
        # map weathercode to a simple label
        code = current.get('weathercode')
        weather = _weathercode_to_text(code)

    # Extract humidity and precipitation for the matching hour from hourly arrays
    hourly = payload.get('hourly', {})
    times = hourly.get('time', [])
    temps = hourly.get('temperature_2m', [])
    hums = hourly.get('relativehumidity_2m', [])
    precs = hourly.get('precipitation', [])

    # Try to find the index for current time
    current_time = current.get('time') if current else None
    if current_time and times:
        try:
            idx = times.index(current_time)
            if idx < len(hums):
                humidity = hums[idx]
            if idx < len(precs):
                rainfall = precs[idx]
        except ValueError:
            # fallback to last available values
            if hums:
                humidity = hums[-1]
            if precs:
                rainfall = precs[-1]
    else:
        if hums:
            humidity = hums[-1]
        if precs:
            rainfall = precs[-1]

    # Ensure types and rounding for easier frontend display
    result = {
        'temperature': round(temperature, 1) if isinstance(temperature, (int, float)) else None,
        'humidity': int(round(humidity)) if isinstance(humidity, (int, float)) else None,
        'rainfall': round(float(rainfall), 2) if rainfall is not None else 0.0,
        'weather': weather,
    }
    return result


def _weathercode_to_text(code):
    """Map Open-Meteo weathercode to a human-friendly text label."""
    mapping = {
        0: 'Clear',
        1: 'Mainly Clear',
        2: 'Partly Cloudy',
        3: 'Overcast',
        45: 'Fog',
        48: 'Depositing rime fog',
        51: 'Light Drizzle',
        53: 'Moderate Drizzle',
        55: 'Dense Drizzle',
        61: 'Slight Rain',
        63: 'Moderate Rain',
        65: 'Heavy Rain',
        71: 'Slight Snow',
        73: 'Moderate Snow',
        75: 'Heavy Snow',
        80: 'Rain Showers',
        81: 'Heavy Rain Showers',
        95: 'Thunderstorm',
    }
    try:
        return mapping.get(int(code), 'Unknown')
    except Exception:
        return 'Unknown'
