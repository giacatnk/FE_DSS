import os
import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import datetime
import pandas as pd

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'versions')
LATEST_DIR = os.path.join(BASE_DIR, 'models', 'latest')

# Create directories if they don't exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LATEST_DIR, exist_ok=True)

def load_data():
    """Load and preprocess the data"""
    # Assuming you have a CSV file with the mock data
    df = pd.read_csv('data/mock.csv')
    
    # Extract features
    features = df.drop(['label'], axis=1).values
    labels = df['label'].values
    
    return features, labels

def train_model():
    """Train a new model using MLPClassifier"""
    try:
        # Load data
        X, y = load_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        train_accuracy = accuracy_score(y_train, model.predict(X_train))
        test_accuracy = accuracy_score(y_test, model.predict(X_test))
        
        # Create version string
        version = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        model_path = os.path.join(MODELS_DIR, f'model_{version}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Update latest model
        latest_path = os.path.join(LATEST_DIR, 'model.pkl')
        with open(latest_path, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"Successfully trained model:")
        print(f"Version: {version}")
        print(f"Train Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Model saved to: {model_path}")
        
        return version
        
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return None

def load_model(version=None):
    """Load a specific model version or the latest model"""
    try:
        if version:
            model_path = os.path.join(MODELS_DIR, f'model_{version}.pkl')
        else:
            model_path = os.path.join(LATEST_DIR, 'model.pkl')
            
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def make_prediction(data, version=None):
    """Make a prediction using a specific model version"""
    try:
        model = load_model(version)
        if model is None:
            return {'error': 'Model not found'}
            
        prediction = model.predict([data])[0]
        probabilities = model.predict_proba([data])[0]
        confidence = probabilities[1] if prediction else probabilities[0]
        
        return {
            'prediction': bool(prediction),
            'confidence': float(confidence),
            'model_version': version
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    # Train a new model when script is run directly
    train_model()
