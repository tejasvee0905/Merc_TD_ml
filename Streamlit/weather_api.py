# Weather Prediction API using Flask
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
from database import init_database, save_prediction, get_all_predictions, get_recent_predictions, get_prediction_stats

app = Flask(__name__)

# Initialize database
init_database()

# Load the trained model
try:
    model = joblib.load("weather_model.pkl")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('weather_index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Create DataFrame with input features
        input_data = pd.DataFrame({
            'humidity_percent': [float(data.get('humidity_percent', 0))],
            'pressure_hpa': [float(data.get('pressure_hpa', 0))],
            'wind_speed_kmph': [float(data.get('wind_speed_kmph', 0))],
            'cloud_cover_percent': [float(data.get('cloud_cover_percent', 0))],
            'rainfall_mm': [float(data.get('rainfall_mm', 0))],
            'sunshine_hours': [float(data.get('sunshine_hours', 0))]
        })
        
        # Make prediction
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
            
        prediction = model.predict(input_data)
        predicted_temp = float(prediction[0])
        
        # Save prediction to database
        prediction_data = {
            'humidity_percent': float(data.get('humidity_percent', 0)),
            'pressure_hpa': float(data.get('pressure_hpa', 0)),
            'wind_speed_kmph': float(data.get('wind_speed_kmph', 0)),
            'cloud_cover_percent': float(data.get('cloud_cover_percent', 0)),
            'rainfall_mm': float(data.get('rainfall_mm', 0)),
            'sunshine_hours': float(data.get('sunshine_hours', 0)),
            'predicted_temperature': round(predicted_temp, 2)
        }
        
        prediction_id = save_prediction(prediction_data)
        
        return jsonify({
            'predicted_temperature': round(predicted_temp, 2),
            'prediction_id': prediction_id,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/history', methods=['GET'])
def history():
    """Get all prediction history"""
    try:
        df = get_all_predictions()
        return jsonify({
            'status': 'success',
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/recent', methods=['GET'])
def recent():
    """Get recent predictions"""
    try:
        limit = request.args.get('limit', 10, type=int)
        df = get_recent_predictions(limit)
        return jsonify({
            'status': 'success',
            'data': df.to_dict('records')
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/stats', methods=['GET'])
def stats():
    """Get prediction statistics"""
    try:
        stats = get_prediction_stats()
        return jsonify({
            'status': 'success',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
