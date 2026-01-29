# Database setup and management for Weather Predictions
import sqlite3
from datetime import datetime
import pandas as pd

DB_NAME = "weather_predictions.db"

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            humidity_percent REAL,
            pressure_hpa REAL,
            wind_speed_kmph REAL,
            cloud_cover_percent REAL,
            rainfall_mm REAL,
            sunshine_hours REAL,
            predicted_temperature REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_prediction(data):
    """
    Save a prediction to the database
    
    Args:
        data (dict): Dictionary containing input features and predicted temperature
    
    Returns:
        int: ID of the saved prediction
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (
            humidity_percent, pressure_hpa, wind_speed_kmph,
            cloud_cover_percent, rainfall_mm, sunshine_hours,
            predicted_temperature
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['humidity_percent'],
        data['pressure_hpa'],
        data['wind_speed_kmph'],
        data['cloud_cover_percent'],
        data['rainfall_mm'],
        data['sunshine_hours'],
        data['predicted_temperature']
    ))
    
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return prediction_id

def get_all_predictions():
    """
    Retrieve all predictions from the database
    
    Returns:
        pandas.DataFrame: DataFrame containing all predictions
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def get_recent_predictions(limit=10):
    """
    Retrieve recent predictions from the database
    
    Args:
        limit (int): Number of recent predictions to retrieve
    
    Returns:
        pandas.DataFrame: DataFrame containing recent predictions
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        f"SELECT * FROM predictions ORDER BY timestamp DESC LIMIT {limit}", 
        conn
    )
    conn.close()
    return df

def get_prediction_stats():
    """
    Get statistics about predictions
    
    Returns:
        dict: Dictionary containing prediction statistics
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total_predictions,
            AVG(predicted_temperature) as avg_temperature,
            MIN(predicted_temperature) as min_temperature,
            MAX(predicted_temperature) as max_temperature,
            AVG(humidity_percent) as avg_humidity,
            AVG(rainfall_mm) as avg_rainfall
        FROM predictions
    ''')
    
    row = cursor.fetchone()
    conn.close()
    
    if row[0] == 0:  # No predictions yet
        return {
            'total_predictions': 0,
            'avg_temperature': 0,
            'min_temperature': 0,
            'max_temperature': 0,
            'avg_humidity': 0,
            'avg_rainfall': 0
        }
    
    return {
        'total_predictions': row[0],
        'avg_temperature': round(row[1], 2) if row[1] else 0,
        'min_temperature': round(row[2], 2) if row[2] else 0,
        'max_temperature': round(row[3], 2) if row[3] else 0,
        'avg_humidity': round(row[4], 2) if row[4] else 0,
        'avg_rainfall': round(row[5], 2) if row[5] else 0
    }

def delete_all_predictions():
    """Delete all predictions from the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
    print("All predictions deleted!")

if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("\nDatabase schema created successfully!")
    print(f"Database file: {DB_NAME}")
