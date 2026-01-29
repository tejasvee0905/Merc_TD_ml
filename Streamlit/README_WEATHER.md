# Weather Temperature Prediction System

A complete machine learning system for predicting temperature based on weather conditions, with Flask API and Streamlit frontend.

## 📁 Files Structure

```
Streamlit/
├── weather_model.py          # ML model training script
├── weather_model.pkl         # Saved trained model (generated)
├── weather_api.py            # Flask API server
├── weather_streamlit.py      # Streamlit frontend
├── sales.csv                 # Sales data
├── weather_linear.csv        # Weather dataset (in ../Regression/)
└── templates/
    └── weather_index.html    # Flask HTML template
```

## 🚀 Setup and Installation

### 1. Install Required Packages

```bash
pip install pandas numpy scikit-learn joblib flask streamlit requests plotly
```

### 2. Train the Model

First, train the model and save it:

```bash
python weather_model.py
```

This will:
- Load the weather dataset
- Train a Linear Regression model with preprocessing pipeline
- Save the model as `weather_model.pkl`
- Display performance metrics

## 🎯 Running the System

You need to run **TWO** components:

### Option 1: Streamlit Frontend (Recommended)

**Step 1: Start the Flask API**
Open a terminal and run:
```bash
python weather_api.py
```
The API will start on `http://localhost:5000`

**Step 2: Start Streamlit Frontend**
Open another terminal and run:
```bash
streamlit run weather_streamlit.py
```
The Streamlit app will open in your browser at `http://localhost:8501`

### Option 2: Flask Web Interface

**Step 1: Start the Flask API**
```bash
python weather_api.py
```
Then open `http://localhost:5000` in your browser.

## 📊 Features

### ML Model
- **Algorithm**: Linear Regression
- **Features**: 
  - Humidity (%)
  - Atmospheric Pressure (hPa)
  - Wind Speed (km/h)
  - Cloud Cover (%)
  - Rainfall (mm)
  - Sunshine Hours
- **Target**: Temperature (°C)
- **Preprocessing**: Mean imputation + Standard scaling

### Flask API
- **Endpoint**: `/predict` (POST)
- **Health Check**: `/health` (GET)
- **Input Format**: JSON
```json
{
  "humidity_percent": 60.0,
  "pressure_hpa": 1013.0,
  "wind_speed_kmph": 15.0,
  "cloud_cover_percent": 45.0,
  "rainfall_mm": 5.0,
  "sunshine_hours": 6.5
}
```
- **Output Format**: JSON
```json
{
  "predicted_temperature": 58.42,
  "status": "success"
}
```

### Streamlit Frontend
- **Dark Theme**: Minimal and modern design
- **Interactive Sliders**: Easy parameter adjustment
- **Real-time Prediction**: Instant temperature forecast
- **Visualizations**:
  - Temperature gauge
  - Parameter overview bar chart
  - Weather condition indicators
- **Analysis**: Temperature interpretation

## 🧪 Testing the API

Using curl:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "humidity_percent": 85.0,
    "pressure_hpa": 1013.0,
    "wind_speed_kmph": 15.0,
    "cloud_cover_percent": 80.0,
    "rainfall_mm": 25.0,
    "sunshine_hours": 2.0
  }'
```

Using Python:
```python
import requests

data = {
    'humidity_percent': 60.0,
    'pressure_hpa': 1013.0,
    'wind_speed_kmph': 15.0,
    'cloud_cover_percent': 45.0,
    'rainfall_mm': 5.0,
    'sunshine_hours': 6.5
}

response = requests.post('http://localhost:5000/predict', json=data)
print(response.json())
```

## 📈 Model Performance

After training, you'll see metrics like:
- **R² Score**: Model accuracy (closer to 1 is better)
- **RMSE**: Root Mean Square Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)

## 🎨 UI Features

### Streamlit Dashboard:
- **Sidebar Controls**: Adjust all weather parameters
- **Metric Cards**: Display current conditions
- **Weather Status**: Auto-detect weather conditions
- **Temperature Gauge**: Visual temperature display
- **Parameter Chart**: Bar chart of input values
- **Analysis Section**: Temperature interpretation

## 🔧 Troubleshooting

### API Connection Error
If Streamlit shows "Cannot connect to API":
1. Make sure Flask API is running: `python weather_api.py`
2. Check if port 5000 is available
3. Verify `weather_model.pkl` exists

### Model Not Found
If you get "Model not loaded":
1. Run `python weather_model.py` first
2. Make sure `weather_model.pkl` is in the same directory

### Module Not Found
Install missing packages:
```bash
pip install <package-name>
```

## 📝 Sample Predictions

**Rainy Day** (High humidity, rainfall):
- Humidity: 85%, Pressure: 1013 hPa, Wind: 15 km/h
- Cloud Cover: 80%, Rainfall: 25mm, Sunshine: 2hrs
- **Expected**: Cool temperature (~50-55°C)

**Sunny Day** (Low humidity, high sunshine):
- Humidity: 25%, Pressure: 1015 hPa, Wind: 8 km/h
- Cloud Cover: 10%, Rainfall: 0mm, Sunshine: 11hrs
- **Expected**: Warm temperature (~65-70°C)

## 🌟 Next Steps

- Add more ML models (Random Forest, XGBoost)
- Include historical predictions
- Add data visualization dashboard
- Deploy to cloud (Heroku, AWS, Azure)
- Add authentication
- Implement model retraining pipeline

## 📄 License

This project is for educational purposes.
