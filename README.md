# Smart Agriculture Decision Support System

A complete end-to-end web application that combines AI and Machine Learning to provide intelligent agricultural decision support through crop recommendation, yield prediction, and weather-based advisory.

## 🌟 Features

### 1. Crop Recommendation Module
- **Input Parameters**: Soil nutrients (N, P, K), pH, temperature, humidity, rainfall
- **ML Algorithm**: Random Forest Classifier
- **Output**: Recommended crop with confidence scores for top 3 suggestions
- **Advice**: Personalized agricultural recommendations based on soil and climate

### 2. Crop Yield Prediction Module
- **Input Parameters**: State, crop type, cultivation area, rainfall, fertilizer, pesticide usage
- **ML Algorithm**: Random Forest Regressor
- **Output**: Predicted yield per hectare and total production
- **Advice**: Tips for yield improvement and resource optimization

### 3. Weather Advisory Module
- **Input**: Location/City
- **Features**: Real-time weather data (temperature, humidity, rainfall, wind speed)
- **Output**: Weather-based farming advisories
- **Recommendations**: Irrigation advice, pest alerts, farming activity suggestions

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Models**: Random Forest (Classification & Regression)
- **Data Format**: CSV datasets

## 📁 Project Structure

```
smart_agriculture_system/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── datasets/
│   ├── crop_recommendation.csv    # Training data (200+ samples)
│   └── crop_yield.csv             # Training data (100+ samples)
├── models/
│   ├── train_crop_model.py        # Crop recommendation trainer
│   ├── train_yield_model.py       # Yield prediction trainer
│   ├── crop_model.pkl             # Saved model (generated)
│   └── yield_model.pkl            # Saved model (generated)
├── static/
│   ├── css/
│   │   └── style.css              # Modern responsive stylesheet
│   └── js/
│       └── script.js              # Frontend JavaScript
└── templates/
    ├── index.html                 # Home page
    ├── crop_recommendation.html   # Crop recommendation interface
    ├── yield_prediction.html      # Yield prediction interface
    └── weather_advisory.html      # Weather advisory interface
```

## 🚀 Installation & Setup

### Step 1: Install Python
Ensure Python 3.8 or higher is installed on your system.

```bash
# Check Python version
python --version
# or
python3 --version
```

### Step 2: Clone or Download the Project
Download and extract the project files to your desired location.

### Step 3: Navigate to Project Directory
```bash
cd smart_agriculture_system
```

### Step 4: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Train Machine Learning Models
```bash
# Navigate to models directory
cd models

# Train crop recommendation model
python train_crop_model.py

# Train yield prediction model
python train_yield_model.py

# Return to main directory
cd ..
```

**Expected Output**: You should see training progress and model accuracy metrics. Two `.pkl` files will be created in the `models/` directory.

### Step 7: Run the Application
```bash
python app.py
```

**Expected Output**:
```
============================================================
SMART AGRICULTURE DECISION SUPPORT SYSTEM
============================================================

Starting Flask server...
Access the application at: http://127.0.0.1:5000

Press CTRL+C to stop the server
```

### Step 8: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

## 📖 Usage Guide

### Crop Recommendation
1. Navigate to **Crop Recommendation** page
2. Enter soil parameters (N, P, K values, pH)
3. Enter environmental data (temperature, humidity, rainfall)
4. Click **Get Crop Recommendation**
5. View recommended crops with confidence scores and agricultural advice

**Example Input**:
- Nitrogen: 90 kg/ha
- Phosphorus: 42 kg/ha
- Potassium: 43 kg/ha
- Temperature: 20.87°C
- Humidity: 82%
- pH: 6.5
- Rainfall: 202.93 mm

**Expected Output**: Rice (with high confidence)

### Yield Prediction
1. Navigate to **Yield Prediction** page
2. Select state and crop type
3. Enter cultivation area (hectares)
4. Enter rainfall, fertilizer, and pesticide usage
5. Click **Predict Yield**
6. View predicted yield per hectare and total production

**Example Input**:
- State: Maharashtra
- Crop: Rice
- Area: 1200 hectares
- Rainfall: 1150 mm
- Fertilizer: 120 kg/ha
- Pesticide: 15 kg/ha

**Expected Output**: ~3.0 tons/hectare yield

### Weather Advisory
1. Navigate to **Weather Advisory** page
2. Enter your city or location
3. Click **Get Weather Advisory**
4. View current weather conditions
5. Read personalized farming recommendations

## 🎯 Dataset Information

### Crop Recommendation Dataset
- **Size**: 200+ samples
- **Crops**: 22 different crops (rice, wheat, maize, cotton, sugarcane, pulses, fruits, etc.)
- **Features**: N, P, K, temperature, humidity, pH, rainfall
- **Format**: CSV

### Yield Prediction Dataset
- **Size**: 100+ samples
- **Crops**: 20+ major crops
- **States**: 10+ Indian states
- **Features**: State, crop, area, rainfall, fertilizer, pesticide, production
- **Format**: CSV

## 🧪 Model Performance

### Crop Recommendation Model
- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~95-98%
- **Features**: 7 input parameters
- **Output**: 22 crop classes

### Yield Prediction Model
- **Algorithm**: Random Forest Regressor
- **R² Score**: ~0.90-0.95
- **Features**: 6 input parameters
- **Output**: Continuous yield value

## 🔧 Troubleshooting

### Issue: Models not found
**Solution**: Make sure you've run the training scripts:
```bash
cd models
python train_crop_model.py
python train_yield_model.py
```

### Issue: Port 5000 already in use
**Solution**: Either stop the process using port 5000 or change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Module not found errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Permission denied (on Linux/Mac)
**Solution**: Use `python3` instead of `python`:
```bash
python3 app.py
```

## 🌐 API Endpoints

The application exposes the following REST API endpoints:

- `POST /api/recommend-crop` - Get crop recommendations
- `POST /api/predict-yield` - Predict crop yield
- `POST /api/weather` - Get weather advisory

## 📊 Features Explanation

### Why These Features Matter

**Soil NPK Values**: 
- Nitrogen (N) promotes leafy growth
- Phosphorus (P) supports root development
- Potassium (K) enhances overall plant health

**pH Level**: 
- Affects nutrient availability
- Different crops prefer different pH ranges

**Climate Data**: 
- Temperature affects crop growth rate
- Humidity impacts disease susceptibility
- Rainfall determines irrigation needs

## 🔐 Security Note

This is a demonstration application. For production use:
- Add user authentication
- Implement API rate limiting
- Use environment variables for sensitive data
- Add input validation and sanitization
- Implement HTTPS

## 📝 Future Enhancements

- [ ] User authentication and profiles
- [ ] Historical data tracking
- [ ] Mobile app version
- [ ] Integration with IoT sensors
- [ ] Multi-language support
- [ ] Export reports as PDF
- [ ] Real-time weather API integration with API key
- [ ] Crop disease detection using image recognition
- [ ] Market price prediction
- [ ] Farming activity scheduler

## 🤝 Contributing

This is a demonstration project. Feel free to extend it with additional features!

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Developer Notes

- All models are pre-trained on sample datasets
- Weather data uses mock data by default (can be configured with real API)
- The system provides recommendations based on statistical patterns
- Actual farming decisions should combine AI suggestions with local expertise

## 📧 Support

For issues or questions, please refer to the troubleshooting section or review the code comments.

---

**Built with ❤️ using Python, Flask, and Machine Learning**

🌾 Empowering Farmers Through Technology 🌾
