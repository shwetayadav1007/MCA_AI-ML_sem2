import streamlit as st
from pathlib import Path
import pandas as pd
from api.weather_api import fetch_current_weather, fetch_weather_data
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'groundwater.csv'

st.set_page_config(page_title='Smart Groundwater Prediction Dashboard', layout='wide')
st.title('Smart Groundwater Prediction Dashboard')

# Live weather panel
st.markdown('## Live weather')
try:
    weather = fetch_current_weather('22.57', '88.36')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Temperature (°C)', weather.get('temperature'))
    col2.metric('Humidity (%)', weather.get('humidity'))
    col3.metric('Rainfall (mm)', weather.get('rainfall'))
    col4.metric('Condition', weather.get('weather'))

    # warning
    temp_val = weather.get('temperature')
    if temp_val is not None and temp_val > 40:
        st.warning('High temperature detected: exercise caution — temperature exceeds 40°C')

    # temperature trend (last 24 hours)
    hourly = fetch_weather_data('22.57', '88.36')
    temps = hourly.get('hourly', {}).get('temperature_2m', [])
    times = hourly.get('hourly', {}).get('time', [])
    if temps and times:
        dfw = pd.DataFrame({'time': times[-24:], 'temperature': temps[-24:]})
        dfw['time'] = pd.to_datetime(dfw['time'])
        fig = px.line(dfw, x='time', y='temperature', title='Temperature (last 24 hours)')
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f'Could not load live weather: {e}')

if not DATA_PATH.exists():
    st.warning('Data file not found. Add data/raw/groundwater.csv to load the dataset.')
else:
    df = pd.read_csv(DATA_PATH)
    st.markdown('### Dataset overview')
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown('### Summary statistics')
    st.dataframe(df.describe())

    st.markdown('### Rainfall and groundwater level trend')
    st.line_chart(df[['Rainfall', 'Groundwater_Level']].rename(columns={'Groundwater_Level': 'Groundwater Level'}))

    st.markdown('### Water usage analysis')
    st.bar_chart(df[['Water_Usage', 'Groundwater_Level']].rename(columns={'Water_Usage': 'Water Usage', 'Groundwater_Level': 'Groundwater Level'}))

    st.markdown('### Regional risk segmentation')
    if 'Region' in df.columns and 'Groundwater_Level' in df.columns:
        region_summary = df.groupby('Region')[['Groundwater_Level']].mean().reset_index()
        region_summary.columns = ['Region', 'Average Groundwater Level']
        st.dataframe(region_summary)

    st.markdown('### Soil moisture distribution')
    if 'Soil_Moisture' in df.columns:
        st.area_chart(df[['Soil_Moisture']])
