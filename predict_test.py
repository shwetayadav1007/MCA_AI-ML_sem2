import requests

url = 'http://127.0.0.1:5000/predict'
payload = {
    'Rainfall': 120,
    'Temperature': 30,
    'Humidity': 70,
    'Soil_Moisture': 35,
    'Water_Usage': 210,
    'Season': 'Summer'
}
response = requests.post(url, json=payload, timeout=10)
print('status', response.status_code)
print(response.text)
