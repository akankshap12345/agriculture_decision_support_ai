"""
Crop Recommendation Model Training Script
Uses Random Forest Classifier to recommend crops based on soil and environmental parameters
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def train_crop_recommendation_model():
    """Train and save the crop recommendation model"""
    
    print("=" * 60)
    print("CROP RECOMMENDATION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    print("\n[1] Loading dataset...")
    df = pd.read_csv('../datasets/crop_recommendation.csv')
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Crops in dataset: {df['label'].unique()}")
    print(f"Number of unique crops: {df['label'].nunique()}")
    
    # Prepare features and target
    print("\n[2] Preparing features and target...")
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Split data
    print("\n[3] Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    # Train model
    print("\n[4] Training Random Forest Classifier...")
    model = RandomForestClassifier(
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
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Feature importance
    print("\n[6] Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))
    
    # Save model
    print("\n[7] Saving model...")
    model_path = 'crop_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to: {model_path}")
    
    # Test prediction
    print("\n[8] Testing model with sample prediction...")
    sample_input = [[90, 42, 43, 20.87, 82.00, 6.50, 202.93]]  # Rice parameters
    prediction = model.predict(sample_input)
    print(f"Sample input: N=90, P=42, K=43, Temp=20.87, Humidity=82, pH=6.5, Rainfall=202.93")
    print(f"Predicted crop: {prediction[0]}")
    
    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return model

if __name__ == "__main__":
    # Change to models directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_crop_recommendation_model()
