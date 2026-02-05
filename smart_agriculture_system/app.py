"""
Smart Agriculture Decision Support System
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
import requests
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
WEATHER_API_KEY = 'demo'  # Using demo mode for offline capability
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Load ML models
def load_models():
    """Load trained ML models"""
    global crop_model, yield_model_data
    
    try:
        # Load crop recommendation model
        with open('models/crop_model.pkl', 'rb') as f:
            crop_model = pickle.load(f)
        print("✓ Crop recommendation model loaded successfully")
        
        # Load yield prediction model
        with open('models/yield_model.pkl', 'rb') as f:
            yield_model_data = pickle.load(f)
        print("✓ Yield prediction model loaded successfully")
        
    except FileNotFoundError as e:
        print(f"Error: Model file not found - {e}")
        print("Please train the models first by running:")
        print("  python models/train_crop_model.py")
        print("  python models/train_yield_model.py")
        exit(1)

# Load models on startup
load_models()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/crop-recommendation')
def crop_recommendation_page():
    """Crop recommendation page"""
    return render_template('crop_recommendation.html')

@app.route('/yield-prediction')
def yield_prediction_page():
    """Yield prediction page"""
    # Get available states and crops from the model
    states = list(yield_model_data['state_encoder'].classes_)
    crops = list(yield_model_data['crop_encoder'].classes_)
    return render_template('yield_prediction.html', states=states, crops=crops)

@app.route('/weather-advisory')
def weather_advisory_page():
    """Weather advisory page"""
    return render_template('weather_advisory.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/recommend-crop', methods=['POST'])
def recommend_crop():
    """API endpoint for crop recommendation"""
    try:
        data = request.get_json()
        
        # Extract features
        features = np.array([[
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]])
        
        # Make prediction
        prediction = crop_model.predict(features)[0]
        
        # Get prediction probabilities
        probabilities = crop_model.predict_proba(features)[0]
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        
        recommendations = []
        for idx in top_3_indices:
            crop_name = crop_model.classes_[idx]
            confidence = float(probabilities[idx] * 100)
            recommendations.append({
                'crop': crop_name,
                'confidence': round(confidence, 2)
            })
        
        # Generate advice based on inputs
        advice = generate_crop_advice(data, prediction)
        
        return jsonify({
            'success': True,
            'recommended_crop': prediction,
            'top_recommendations': recommendations,
            'advice': advice,
            'input_parameters': {
                'Nitrogen (N)': f"{data['nitrogen']} kg/ha",
                'Phosphorus (P)': f"{data['phosphorus']} kg/ha",
                'Potassium (K)': f"{data['potassium']} kg/ha",
                'Temperature': f"{data['temperature']}°C",
                'Humidity': f"{data['humidity']}%",
                'pH': data['ph'],
                'Rainfall': f"{data['rainfall']} mm"
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/predict-yield', methods=['POST'])
def predict_yield():
    """API endpoint for yield prediction"""
    try:
        data = request.get_json()
        
        # Encode categorical variables
        state_encoded = yield_model_data['state_encoder'].transform([data['state']])[0]
        crop_encoded = yield_model_data['crop_encoder'].transform([data['crop']])[0]
        
        # Prepare features
        features = np.array([[
            state_encoded,
            crop_encoded,
            float(data['area']),
            float(data['rainfall']),
            float(data['fertilizer']),
            float(data['pesticide'])
        ]])
        
        # Make prediction
        model = yield_model_data['model']
        predicted_yield = model.predict(features)[0]
        total_production = predicted_yield * float(data['area'])
        
        # Generate advice
        advice = generate_yield_advice(data, predicted_yield)
        
        return jsonify({
            'success': True,
            'predicted_yield': round(predicted_yield, 2),
            'total_production': round(total_production, 2),
            'advice': advice,
            'input_parameters': {
                'State': data['state'],
                'Crop': data['crop'],
                'Area': f"{data['area']} hectares",
                'Annual Rainfall': f"{data['rainfall']} mm",
                'Fertilizer': f"{data['fertilizer']} kg/ha",
                'Pesticide': f"{data['pesticide']} kg/ha"
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """API endpoint for weather information and advisory"""
    try:
        data = request.get_json()
        city = data.get('city', 'Mumbai')
        
        # Try to fetch real weather data
        weather_data = fetch_weather_data(city)
        
        if not weather_data:
            # Use mock data if API fails
            weather_data = get_mock_weather_data(city)
        
        # Generate advisory based on weather
        advisory = generate_weather_advisory(weather_data)
        
        return jsonify({
            'success': True,
            'weather': weather_data,
            'advisory': advisory
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ==================== HELPER FUNCTIONS ====================

def fetch_weather_data(city):
    """Fetch real weather data from OpenWeather API"""
    try:
        # Note: In production, use a real API key
        # For demo purposes, we'll use mock data
        return None
    except:
        return None

def get_mock_weather_data(city):
    """Generate mock weather data for demo purposes"""
    import random
    
    mock_data = {
        'city': city,
        'temperature': round(25 + random.uniform(-5, 10), 1),
        'humidity': round(60 + random.uniform(-20, 30), 1),
        'rainfall': round(random.uniform(0, 50), 1),
        'wind_speed': round(random.uniform(5, 20), 1),
        'description': random.choice(['Clear sky', 'Partly cloudy', 'Cloudy', 'Light rain', 'Sunny']),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return mock_data

def generate_crop_advice(input_data, recommended_crop):
    """Generate agricultural advice based on inputs"""
    advice = []
    
    # pH advice
    ph = float(input_data['ph'])
    if ph < 5.5:
        advice.append("⚠️ Soil is too acidic. Consider adding lime to raise pH.")
    elif ph > 8.0:
        advice.append("⚠️ Soil is too alkaline. Consider adding sulfur to lower pH.")
    else:
        advice.append("✓ Soil pH is optimal for most crops.")
    
    # NPK advice
    n = float(input_data['nitrogen'])
    p = float(input_data['phosphorus'])
    k = float(input_data['potassium'])
    
    if n < 50:
        advice.append("🌱 Low nitrogen levels. Consider adding urea or composted manure.")
    if p < 30:
        advice.append("🌱 Low phosphorus levels. Consider adding bone meal or rock phosphate.")
    if k < 30:
        advice.append("🌱 Low potassium levels. Consider adding potash or wood ash.")
    
    # Temperature advice
    temp = float(input_data['temperature'])
    if temp < 15:
        advice.append("❄️ Temperature is low. Consider cold-resistant crops or greenhouse farming.")
    elif temp > 35:
        advice.append("☀️ Temperature is high. Ensure adequate irrigation and mulching.")
    
    # Rainfall advice
    rainfall = float(input_data['rainfall'])
    if rainfall < 100:
        advice.append("💧 Low rainfall area. Ensure proper irrigation system is in place.")
    elif rainfall > 300:
        advice.append("🌧️ High rainfall area. Ensure proper drainage to prevent waterlogging.")
    
    # Crop-specific advice
    advice.append(f"🌾 {recommended_crop.capitalize()} is well-suited for your soil and climate conditions.")
    
    return advice

def generate_yield_advice(input_data, predicted_yield):
    """Generate advice for yield improvement"""
    advice = []
    
    crop = input_data['crop']
    rainfall = float(input_data['rainfall'])
    fertilizer = float(input_data['fertilizer'])
    
    # General advice
    advice.append(f"📊 Expected yield: {predicted_yield:.2f} tons per hectare")
    
    # Fertilizer advice
    if fertilizer < 100:
        advice.append("🌱 Consider increasing fertilizer application for better yield.")
    elif fertilizer > 200:
        advice.append("⚠️ High fertilizer use. Ensure it's balanced to avoid soil degradation.")
    else:
        advice.append("✓ Fertilizer application is within optimal range.")
    
    # Rainfall advice
    if rainfall < 600:
        advice.append("💧 Supplement with irrigation during dry periods.")
    elif rainfall > 1500:
        advice.append("🌧️ Ensure proper drainage systems to prevent crop damage.")
    
    # Yield improvement tips
    advice.append("💡 Tips for better yield:")
    advice.append("  • Use quality seeds from certified sources")
    advice.append("  • Implement crop rotation practices")
    advice.append("  • Monitor and control pests regularly")
    advice.append("  • Maintain optimal soil moisture levels")
    
    return advice

def generate_weather_advisory(weather_data):
    """Generate weather-based agricultural advisory"""
    advisory = []
    
    temp = weather_data['temperature']
    humidity = weather_data['humidity']
    rainfall = weather_data['rainfall']
    
    # Temperature advisory
    if temp > 35:
        advisory.append({
            'type': 'warning',
            'title': 'High Temperature Alert',
            'message': 'Extreme heat detected. Increase irrigation frequency and provide shade for sensitive crops.'
        })
    elif temp < 10:
        advisory.append({
            'type': 'warning',
            'title': 'Low Temperature Alert',
            'message': 'Cold weather detected. Protect crops from frost damage using covers or mulching.'
        })
    else:
        advisory.append({
            'type': 'success',
            'title': 'Optimal Temperature',
            'message': 'Temperature conditions are favorable for crop growth.'
        })
    
    # Humidity advisory
    if humidity > 85:
        advisory.append({
            'type': 'warning',
            'title': 'High Humidity',
            'message': 'High humidity may promote fungal diseases. Monitor crops closely and apply fungicides if needed.'
        })
    elif humidity < 40:
        advisory.append({
            'type': 'info',
            'title': 'Low Humidity',
            'message': 'Dry conditions. Ensure adequate irrigation to prevent crop stress.'
        })
    
    # Rainfall advisory
    if rainfall > 20:
        advisory.append({
            'type': 'info',
            'title': 'Rainfall Detected',
            'message': f'Recent rainfall: {rainfall}mm. Postpone irrigation and check drainage systems.'
        })
    elif rainfall == 0:
        advisory.append({
            'type': 'info',
            'title': 'No Rainfall',
            'message': 'No recent rainfall. Maintain regular irrigation schedule.'
        })
    
    # General farming advisory
    advisory.append({
        'type': 'success',
        'title': 'Today\'s Farming Activities',
        'message': get_daily_farming_activity(weather_data)
    })
    
    return advisory

def get_daily_farming_activity(weather_data):
    """Suggest daily farming activities based on weather"""
    temp = weather_data['temperature']
    rainfall = weather_data['rainfall']
    
    if rainfall > 20:
        return "Avoid field operations. Good day for indoor tasks and equipment maintenance."
    elif temp > 35:
        return "Schedule outdoor work for early morning or late evening. Focus on irrigation maintenance."
    elif temp < 15:
        return "Good conditions for harvesting. Check for frost-sensitive crops."
    else:
        return "Ideal conditions for field operations. Good day for planting, weeding, or applying fertilizers."

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SMART AGRICULTURE DECISION SUPPORT SYSTEM")
    print("="*60)
    print("\nStarting Flask server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
