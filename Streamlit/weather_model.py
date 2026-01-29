# Weather Temperature Prediction Model Training
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Load the dataset
print("Loading weather data...")
df = pd.read_csv('../Regression/weather_linear.csv')

# Define features and target
numerical_features = ['humidity_percent', 'pressure_hpa', 'wind_speed_kmph', 
                     'cloud_cover_percent', 'rainfall_mm', 'sunshine_hours']

X = df[numerical_features]
y = df["temperature_c"]

print(f"Feature shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]} samples")
print(f"Test set size: {X_test.shape[0]} samples")

# Create preprocessing and model pipeline
weather_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

print("\nTraining the model...")
weather_pipeline.fit(X_train, y_train)
print("Model training completed!")

# Make predictions
y_train_pred = weather_pipeline.predict(X_train)
y_test_pred = weather_pipeline.predict(X_test)

# Evaluate model performance
print("\n" + "="*50)
print("MODEL PERFORMANCE METRICS")
print("="*50)

print("\nTraining Set:")
print(f"  R² Score: {r2_score(y_train, y_train_pred):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_train, y_train_pred)):.4f}")
print(f"  MAE: {mean_absolute_error(y_train, y_train_pred):.4f}")

print("\nTest Set:")
print(f"  R² Score: {r2_score(y_test, y_test_pred):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_test_pred)):.4f}")
print(f"  MAE: {mean_absolute_error(y_test, y_test_pred):.4f}")

# Save the model
print("\nSaving model...")
joblib.dump(weather_pipeline, "weather_model.pkl")
print("Model saved successfully as 'weather_model.pkl'!")

# Test with sample predictions
print("\n" + "="*50)
print("SAMPLE PREDICTIONS")
print("="*50)

test_case_1 = pd.DataFrame({
    'humidity_percent': [85.0],
    'pressure_hpa': [1013.0],
    'wind_speed_kmph': [15.0],
    'cloud_cover_percent': [80.0],
    'rainfall_mm': [25.0],
    'sunshine_hours': [2.0]
})
print(f"\nRainy Day: {weather_pipeline.predict(test_case_1)[0]:.2f}°C")

test_case_2 = pd.DataFrame({
    'humidity_percent': [25.0],
    'pressure_hpa': [1015.0],
    'wind_speed_kmph': [8.0],
    'cloud_cover_percent': [10.0],
    'rainfall_mm': [0.0],
    'sunshine_hours': [11.0]
})
print(f"Sunny Day: {weather_pipeline.predict(test_case_2)[0]:.2f}°C")
