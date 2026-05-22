import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import joblib
import os

# Set random seed for reproducibility
np.random.seed(42)

def load_and_explore_data(filepath):
    """
    Load the dataset and perform initial exploration.
    """
    # Load dataset
    df = pd.read_csv(filepath)
    
    # Display first 5 rows
    print("First 5 rows:")
    print(df.head())
    print("\n")
    
    # Show dataset information
    print("Dataset Info:")
    print(df.info())
    print("\n")
    
    # Show null values
    print("Null values:")
    print(df.isnull().sum())
    print("\n")
    
    return df

def preprocess_data(df):
    """
    Preprocess the data: handle missing values, remove duplicates, encode categorical variables.
    """
    # Make a copy to avoid modifying original
    df_processed = df.copy()
    
    # Handle missing values - fill with mean for numerical columns
    numerical_cols = df_processed.select_dtypes(include=[np.number]).columns
    df_processed[numerical_cols] = df_processed[numerical_cols].fillna(df_processed[numerical_cols].mean())
    
    # Remove duplicates
    df_processed = df_processed.drop_duplicates()
    
    # Encode categorical variables (Season) using one-hot encoding
    df_processed = pd.get_dummies(df_processed, columns=['Season'], drop_first=False)
    
    # Drop Date and Region if they are not needed for modeling (or keep if they are useful)
    # For this project, we'll drop Date and Region as they are not direct features for prediction
    # But note: we might want to keep Region for some analysis, but for simplicity we drop.
    if 'Date' in df_processed.columns:
        df_processed = df_processed.drop('Date', axis=1)
    if 'Region' in df_processed.columns:
        df_processed = df_processed.drop('Region', axis=1)
    
    return df_processed

def exploratory_data_analysis(df, graphs_dir):
    """
    Perform exploratory data analysis and save graphs.
    """
    # Set style
    sns.set_style("whitegrid")
    
    # 1. Correlation heatmap
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'correlation_heatmap.png'))
    plt.close()
    
    # 2. Rainfall vs Groundwater graph
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Rainfall', y='Groundwater_Level')
    plt.title('Rainfall vs Groundwater Level')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'rainfall_vs_groundwater.png'))
    plt.close()
    
    # 3. Water usage analysis
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Water_Usage', y='Groundwater_Level')
    plt.title('Water Usage vs Groundwater Level')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'water_usage_vs_groundwater.png'))
    plt.close()
    
    # 4. Feature distribution plots
    numerical_features = ['Rainfall', 'Temperature', 'Humidity', 'Soil_Moisture', 'Water_Usage', 'Groundwater_Level']
    plt.figure(figsize=(12, 10))
    for i, feature in enumerate(numerical_features, 1):
        plt.subplot(3, 3, i)
        sns.histplot(df[feature], kde=True)
        plt.title(f'Distribution of {feature}')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'feature_distributions.png'))
    plt.close()
    
    # 5. Pairplot
    sns.pairplot(df[numerical_features])
    plt.suptitle('Pairplot of Numerical Features', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'pairplot.png'))
    plt.close()
    
    # 6. Seasonal groundwater trends (if Season columns exist)
    season_cols = [col for col in df.columns if col.startswith('Season_')]
    if season_cols:
        # We'll create a seasonal trend by averaging groundwater level for each season
        # But note: we have one-hot encoded, so we can't directly get the season.
        # Instead, we'll create a temporary column for season from the one-hot encoded columns.
        df_temp = df.copy()
        # Find which season column is 1 for each row
        season_mapping = {}
        for season_col in season_cols:
            season_name = season_col.split('_')[1]
            season_mapping[season_col] = season_name
        
        # Create a season column
        df_temp['Season'] = df_temp[season_cols].idxmax(axis=1).map(season_mapping)
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_temp, x='Season', y='Groundwater_Level')
        plt.title('Seasonal Groundwater Trends')
        plt.tight_layout()
        plt.savefig(os.path.join(graphs_dir, 'seasonal_groundwater_trends.png'))
        plt.close()

def train_and_evaluate_models(X_train, X_test, y_train, y_test, models_dir):
    """
    Train Linear Regression and XGBoost models, evaluate them, and save the best model.
    """
    # Initialize models
    lr_model = LinearRegression()
    xgb_model = XGBRegressor(random_state=42)
    
    # Train models
    lr_model.fit(X_train, y_train)
    xgb_model.fit(X_train, y_train)
    
    # Predict
    lr_pred = lr_model.predict(X_test)
    xgb_pred = xgb_model.predict(X_test)
    
    # Evaluate Linear Regression
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_mse = mean_squared_error(y_test, lr_pred)
    lr_rmse = np.sqrt(lr_mse)
    lr_r2 = r2_score(y_test, lr_pred)
    
    # Evaluate XGBoost
    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_mse = mean_squared_error(y_test, xgb_pred)
    xgb_rmse = np.sqrt(xgb_mse)
    xgb_r2 = r2_score(y_test, xgb_pred)
    
    # Print evaluation metrics
    print("Linear Regression Metrics:")
    print(f"MAE: {lr_mae:.4f}")
    print(f"MSE: {lr_mse:.4f}")
    print(f"RMSE: {lr_rmse:.4f}")
    print(f"R² Score: {lr_r2:.4f}")
    print("\n")
    
    print("XGBoost Metrics:")
    print(f"MAE: {xgb_mae:.4f}")
    print(f"MSE: {xgb_mse:.4f}")
    print(f"RMSE: {xgb_rmse:.4f}")
    print(f"R² Score: {xgb_r2:.4f}")
    print("\n")
    
    # Determine best model based on R² score
    if lr_r2 > xgb_r2:
        best_model = lr_model
        best_model_name = "Linear Regression"
        best_r2 = lr_r2
    else:
        best_model = xgb_model
        best_model_name = "XGBoost"
        best_r2 = xgb_r2
    
    print(f"Best Model: {best_model_name} with R² Score: {best_r2:.4f}")
    
    # Save models
    joblib.dump(lr_model, os.path.join(models_dir, 'linear_regression_model.pkl'))
    joblib.dump(xgb_model, os.path.join(models_dir, 'xgboost_model.pkl'))
    
    # Save evaluation metrics for later use (optional)
    metrics = {
        'linear_regression': {'mae': lr_mae, 'mse': lr_mse, 'rmse': lr_rmse, 'r2': lr_r2},
        'xgboost': {'mae': xgb_mae, 'mse': xgb_mse, 'rmse': xgb_rmse, 'r2': xgb_r2}
    }
    
    return lr_model, xgb_model, metrics, lr_pred, xgb_pred

def save_prediction_graphs(y_test, lr_pred, xgb_pred, graphs_dir):
    """
    Generate and save prediction-related graphs.
    """
    # 1. Actual vs Predicted graph for both models
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, lr_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Groundwater Level')
    plt.ylabel('Predicted Groundwater Level (LR)')
    plt.title('Actual vs Predicted (Linear Regression)')
    
    plt.subplot(1, 2, 2)
    plt.scatter(y_test, xgb_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Groundwater Level')
    plt.ylabel('Predicted Groundwater Level (XGBoost)')
    plt.title('Actual vs Predicted (XGBoost)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'actual_vs_predicted_both.png'))
    plt.close()
    
    # 2. Model comparison graph (bar chart of metrics)
    metrics = ['MAE', 'MSE', 'RMSE', 'R²']
    lr_values = [mean_absolute_error(y_test, lr_pred), 
                 mean_squared_error(y_test, lr_pred), 
                 np.sqrt(mean_squared_error(y_test, lr_pred)), 
                 r2_score(y_test, lr_pred)]
    xgb_values = [mean_absolute_error(y_test, xgb_pred), 
                  mean_squared_error(y_test, xgb_pred), 
                  np.sqrt(mean_squared_error(y_test, xgb_pred)), 
                  r2_score(y_test, xgb_pred)]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, lr_values, width, label='Linear Regression')
    plt.bar(x + width/2, xgb_values, width, label='XGBoost')
    plt.xlabel('Metrics')
    plt.ylabel('Value')
    plt.title('Model Comparison')
    plt.xticks(x, metrics)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'model_comparison.png'))
    plt.close()
    
    # 3. Error analysis graph (residuals)
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    lr_residuals = y_test - lr_pred
    plt.scatter(lr_pred, lr_residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Groundwater Level (LR)')
    plt.ylabel('Residuals')
    plt.title('Residual Plot (Linear Regression)')
    
    plt.subplot(1, 2, 2)
    xgb_residuals = y_test - xgb_pred
    plt.scatter(xgb_pred, xgb_residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Groundwater Level (XGBoost)')
    plt.ylabel('Residuals')
    plt.title('Residual Plot (XGBoost)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'error_analysis.png'))
    plt.close()
    
    # 4. Feature importance graph for XGBoost
    plt.figure(figsize=(10, 6))
    # Assuming we have the feature names from X_train
    # We'll need to pass feature names to this function, but for now we'll use a placeholder.
    # We'll update this function call in the main block.
    # For now, we'll skip and note that we need to pass feature names.
    pass

def groundwater_risk_category(level):
    """
    Categorize groundwater level into risk categories.
    Based on domain knowledge, we define thresholds (these are example thresholds).
    In a real scenario, these should be defined by domain experts.
    """
    if level > 50:  # Safe threshold (example)
        return "Safe"
    elif level > 30:  # Moderate threshold
        return "Moderate"
    else:
        return "Critical"

def main():
    """
    Main function to run the entire pipeline.
    """
    # Define paths
    data_path = os.path.join('..', 'data', 'raw', 'groundwater.csv')
    models_dir = os.path.join('models')
    graphs_dir = os.path.join('..', 'graphs')
    
    # Ensure directories exist
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)
    
    # Step 1: Load and explore data
    print("Step 1: Loading and exploring data...")
    df = load_and_explore_data(data_path)
    
    # Step 2: Preprocess data
    print("Step 2: Preprocessing data...")
    df_processed = preprocess_data(df)
    
    # Step 3: Exploratory Data Analysis
    print("Step 3: Performing exploratory data analysis...")
    exploratory_data_analysis(df_processed, graphs_dir)
    
    # Step 4: Prepare data for modeling
    print("Step 4: Preparing data for modeling...")
    # Separate features and target
    X = df_processed.drop('Groundwater_Level', axis=1)
    y = df_processed['Groundwater_Level']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Step 5: Train and evaluate models
    print("Step 5: Training and evaluating models...")
    lr_model, xgb_model, metrics, lr_pred, xgb_pred = train_and_evaluate_models(
        X_train, X_test, y_train, y_test, models_dir
    )
    
    # Step 6: Save prediction graphs
    print("Step 6: Saving prediction graphs...")
    save_prediction_graphs(y_test, lr_pred, xgb_pred, graphs_dir)
    
    # Feature importance for XGBoost (we need to generate this separately)
    print("Step 7: Generating feature importance for XGBoost...")
    plt.figure(figsize=(10, 6))
    feature_importance = xgb_model.feature_importances_
    feature_names = X.columns
    # Sort feature importance
    sorted_idx = np.argsort(feature_importance)
    plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
    plt.yticks(range(len(sorted_idx)), np.array(feature_names)[sorted_idx])
    plt.xlabel('Feature Importance')
    plt.title('XGBoost Feature Importance')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'feature_importance_xgboost.png'))
    plt.close()
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()