import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_data(filepath):
    """
    Load data from CSV file.
    """
    return pd.read_csv(filepath)

def save_model(model, filepath):
    """
    Save model to file using joblib.
    """
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")

def load_model(filepath):
    """
    Load model from file using joblib.
    """
    return joblib.load(filepath)

def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }

def plot_actual_vs_predicted(y_true, y_pred, model_name, save_path):
    """
    Plot actual vs predicted values.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Actual Groundwater Level')
    plt.ylabel(f'Predicted Groundwater Level ({model_name})')
    plt.title(f'Actual vs Predicted ({model_name})')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_residuals(y_true, y_pred, model_name, save_path):
    """
    Plot residuals.
    """
    residuals = y_true - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel(f'Predicted Groundwater Level ({model_name})')
    plt.ylabel('Residuals')
    plt.title(f'Residual Plot ({model_name})')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_feature_importance(model, feature_names, save_path):
    """
    Plot feature importance for tree-based models.
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        plt.title(f'Feature Importance ({type(model).__name__})')
        plt.bar(range(len(importances)), importances[indices], align='center')
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    else:
        print(f"Model {type(model).__name__} does not have feature_importances_ attribute")

def ensure_dir(directory):
    """
    Ensure directory exists, create if it doesn't.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)