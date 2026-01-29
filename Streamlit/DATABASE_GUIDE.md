# 🗄️ Database Integration Guide

## Overview

Your weather prediction system now automatically saves all predictions to a SQLite database!

## 📦 Database Schema

**Table: predictions**
- `id` - Unique prediction ID (auto-increment)
- `timestamp` - Date and time of prediction
- `humidity_percent` - Input humidity value
- `pressure_hpa` - Input pressure value
- `wind_speed_kmph` - Input wind speed value
- `cloud_cover_percent` - Input cloud cover value
- `rainfall_mm` - Input rainfall value
- `sunshine_hours` - Input sunshine hours value
- `predicted_temperature` - Output temperature prediction

## 🚀 How It Works

### 1. Automatic Saving
Every time you make a prediction through the Streamlit UI:
1. User inputs weather parameters
2. API makes prediction
3. **Automatically saves** input + prediction to database
4. Returns prediction ID confirmation

### 2. View History
To view all saved predictions:

```bash
cd C:\Users\DWIVEDT\Tejasvee\Td_Merc_Python\Streamlit
streamlit run view_history.py
```

This opens a new Streamlit dashboard showing:
- 📈 Statistics (total predictions, avg temp, min/max)
- 📊 Time series chart of predictions
- 📉 Temperature distribution histogram
- 🔥 Correlation heatmap
- 💧 Scatter plots (humidity vs temp, sunshine vs temp)
- 📝 Recent predictions table
- 💾 CSV export functionality

### 3. API Endpoints

**Save Prediction (Automatic):**
```bash
POST http://localhost:5000/predict
```

**Get All History:**
```bash
GET http://localhost:5000/history
```

**Get Recent Predictions:**
```bash
GET http://localhost:5000/recent?limit=10
```

**Get Statistics:**
```bash
GET http://localhost:5000/stats
```

## 📊 Testing the Database

### 1. Make Some Predictions
- Go to http://localhost:8501
- Adjust the weather parameters
- Click "PREDICT TEMPERATURE"
- Repeat 5-10 times with different values

### 2. View the Data
Run the history viewer:
```bash
streamlit run view_history.py
```

### 3. Check via API
```bash
curl http://localhost:5000/stats
```

## 💾 Database File Location

The database is saved as:
```
C:\Users\DWIVEDT\Tejasvee\Td_Merc_Python\Streamlit\weather_predictions.db
```

## 🔧 Database Management

### View Predictions Programmatically
```python
from database import get_all_predictions, get_prediction_stats

# Get all predictions
df = get_all_predictions()
print(df)

# Get statistics
stats = get_prediction_stats()
print(stats)
```

### Clear All Data
```python
from database import delete_all_predictions

delete_all_predictions()
```

## 📈 Features of History Dashboard

1. **Overview Statistics**
   - Total predictions count
   - Average, min, max temperatures
   - Average humidity and rainfall

2. **Visualizations**
   - Temperature trends over time
   - Distribution of predicted temperatures
   - Feature correlation heatmap
   - Humidity vs Temperature scatter
   - Sunshine vs Temperature scatter

3. **Data Table**
   - Last 20 predictions displayed
   - All columns visible
   - Scrollable view

4. **Export**
   - Download all data as CSV
   - Timestamped filename
   - Ready for Excel/analysis

## 🎯 Use Cases

1. **Track Model Performance**
   - See what inputs generate what outputs
   - Identify patterns in predictions
   - Analyze correlation between features

2. **Historical Analysis**
   - Compare predictions over time
   - Export data for reporting
   - Generate insights

3. **Model Validation**
   - Review unusual predictions
   - Check consistency
   - Identify edge cases

## 🔄 Running Everything

**Terminal 1 - Flask API:**
```bash
cd C:\Users\DWIVEDT\Tejasvee\Td_Merc_Python\Streamlit
python weather_api.py
```

**Terminal 2 - Main Prediction UI:**
```bash
cd C:\Users\DWIVEDT\Tejasvee\Td_Merc_Python\Streamlit
streamlit run weather_streamlit.py
```

**Terminal 3 - History Viewer (Optional):**
```bash
cd C:\Users\DWIVEDT\Tejasvee\Td_Merc_Python\Streamlit
streamlit run view_history.py
```

## ✅ What's Saved

Every prediction saves:
- ✓ All 6 input parameters
- ✓ Predicted temperature
- ✓ Exact timestamp
- ✓ Unique ID

## 🔐 Database Security

- SQLite database (local file)
- No passwords needed
- Can be backed up by copying the .db file
- Can be deleted if needed

## 📱 Next Steps

1. Make 10+ predictions with varied inputs
2. Open the history viewer
3. Explore the visualizations
4. Export the data to CSV
5. Analyze patterns in your predictions

Enjoy your database-powered prediction system! 🎉
