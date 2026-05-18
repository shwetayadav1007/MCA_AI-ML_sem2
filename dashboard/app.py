import streamlit as st
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'groundwater.csv'

st.set_page_config(page_title='Smart Groundwater Prediction Dashboard', layout='wide')
st.title('Smart Groundwater Prediction Dashboard')

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
