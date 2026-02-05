"""
Crop Yield Prediction Model Training Script
Uses Random Forest Regressor to predict crop yield based on various parameters
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pickle
import os

def train_yield_prediction_model():
    """Train and save the yield prediction model"""
    
    print("=" * 60)
    print("CROP YIELD PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    print("\n[1] Loading dataset...")
    df = pd.read_csv('../datasets/crop_yield.csv')
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\nDataset columns: {list(df.columns)}")
    print(f"Crops in dataset: {df['Crop'].unique()}")
    
    # Prepare features
    print("\n[2] Encoding categorical variables...")
    
    # Create label encoders
    le_state = LabelEncoder()
    le_crop = LabelEncoder()
    
    df['State_Encoded'] = le_state.fit_transform(df['State'])
    df['Crop_Encoded'] = le_crop.fit_transform(df['Crop'])
    
    print(f"States encoded: {len(le_state.classes_)} unique states")
    print(f"Crops encoded: {len(le_crop.classes_)} unique crops")
    
    # Select features and target
    feature_columns = ['State_Encoded', 'Crop_Encoded', 'Area', 'Annual_Rainfall', 
                      'Fertilizer', 'Pesticide']
    X = df[feature_columns]
    y = df['Yield']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Target (Yield) - Min: {y.min():.2f}, Max: {y.max():.2f}, Mean: {y.mean():.2f}")
    
    # Split data
    print("\n[3] Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    # Train model
    print("\n[4] Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("Model training completed!")
    
    # Evaluate model
    print("\n[5] Evaluating model performance...")
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    # Feature importance
    print("\n[6] Feature Importance:")
    feature_names = ['State', 'Crop', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide']
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))
    
    # Save model and encoders
    print("\n[7] Saving model and encoders...")
    
    model_data = {
        'model': model,
        'state_encoder': le_state,
        'crop_encoder': le_crop,
        'feature_columns': feature_columns
    }
    
    model_path = 'yield_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    print(f"Model and encoders saved to: {model_path}")
    
    # Test prediction
    print("\n[8] Testing model with sample prediction...")
    # Maharashtra, Rice, 1200 area, 1150 rainfall, 120 fertilizer, 15 pesticide
    state_encoded = le_state.transform(['Maharashtra'])[0]
    crop_encoded = le_crop.transform(['Rice'])[0]
    sample_input = [[state_encoded, crop_encoded, 1200, 1150, 120, 15]]
    
    prediction = model.predict(sample_input)
    print(f"Sample input: State=Maharashtra, Crop=Rice, Area=1200, Rainfall=1150, Fertilizer=120, Pesticide=15")
    print(f"Predicted yield: {prediction[0]:.2f} tons/hectare")
    
    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return model_data

if __name__ == "__main__":
    # Change to models directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_yield_prediction_model()
