# Groundwater Level Prediction System

A full-stack groundwater forecasting platform that combines Python, Flask, machine learning, and a modern dashboard UI to predict groundwater levels and provide risk recommendations.

## Features

- Groundwater level prediction using ML models
- Data preprocessing and model training pipeline
- REST API for prediction and dataset upload
- Dashboard UI with analytics and alerts
- Live weather integration for regional forecasting

## Tech Stack

- Python
- Flask
- Machine Learning (Scikit-learn, XGBoost)
- HTML / CSS / JavaScript
- React + Vite
- Tailwind CSS
- MongoDB support via `pymongo`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shwetanshuyadav/MCA_2_ground_water.git
cd Groundwater_Level_Prediction_System
```

2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Usage

### Backend

From the project root (run these commands where `SIH_Groundwater_Project` is the current working directory):

```bash
# preprocess data and train (optional if model already exists)
python backend/preprocess.py
python backend/train_model.py

# start the backend API (recommended)
python -m backend.api

# alternatively, you can run the script directly
python backend/api.py
```

The backend runs by default on:

- `http://127.0.0.1:5000`

### Frontend

From the `frontend/` folder:

```bash
npm run dev
```

Open the local Vite URL shown in the terminal, usually:

- `http://localhost:5173/`

### Prediction API

Send a POST request to `/predict` with JSON payload:

```json
{
  "Rainfall": 120,
  "Temperature": 30,
  "Humidity": 70,
  "Soil_Moisture": 35,
  "Water_Usage": 210,
  "Season": "Summer"
}
```

## Folder Structure

- `backend/` - Python API, preprocessing, training, prediction logic
- `frontend/` - React dashboard UI and client code
- `dashboard/` - Streamlit analytics dashboard
- `data/` - raw and processed data files
- `models/` - saved model artifacts
- `api/` - external weather API utilities
- `documentation/` - project documentation
- `notebooks/` - exploratory data analysis notebooks

## Best Practices for GitHub

- Keep large datasets and model checkpoints out of Git
- Use `.gitignore` to exclude temporary files and secrets
- Write clean commits with descriptive messages
- Use branches for new features or fixes
- Add a license and clear README for portfolio projects

## Future Improvements

- Add automated tests for backend endpoints
- Add a CI/CD pipeline (GitHub Actions)
- Create a more polished dashboard experience
- Add user authentication and role-based access
- Use Git LFS for large model files and dataset artifacts
