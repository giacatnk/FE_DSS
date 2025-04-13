import logging
from datetime import datetime
from typing import Tuple, Dict, Any
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from src.config import (
    TRAIN_DATA_PATH,
    MODEL_PATH,
    SCALER_PATH,
    MODEL_PARAMS,
    FEATURE_ORDER
)

# Get the logger for this module
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.training_status = "not_started"
        self.last_training_time = None
        self.training_error = None
        self.model_metrics = None

    def load_data(self):
        """Load and preprocess the training data."""
        try:
            df = pd.read_csv(TRAIN_DATA_PATH)
            X = df[FEATURE_ORDER].values
            y = df['label'].values
            logger.info(f"Successfully loaded data from {TRAIN_DATA_PATH}")
            logger.info(f"Data shape: {X.shape}")
            return X, y
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def train_model(self):
        """Train the MLPClassifier model and evaluate its performance."""
        try:
            logger.info("Starting model training...")
            self.training_status = "training"
            self.last_training_time = datetime.now()
            
            # Load and split the data
            X, y = self.load_data()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.05, random_state=42
            )
            logger.info(f"Split data into train: {X_train.shape}, test: {X_test.shape}")
            
            # Scale the features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Initialize and train the model
            self.model = MLPClassifier(**MODEL_PARAMS)
            logger.info("Fitting model with parameters: %s", MODEL_PARAMS)
            self.model.fit(X_train_scaled, y_train)
            logger.info("Model training completed")
            
            # Make predictions and calculate metrics
            y_pred = self.model.predict(X_test_scaled)
            
            # Calculate performance metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            # Store metrics
            self.model_metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'confusion_matrix': conf_matrix.tolist()
            }
            
            # Log performance metrics
            logger.info("Model Performance Metrics:")
            logger.info("Accuracy: %.4f", accuracy)
            logger.info("Precision: %.4f", precision)
            logger.info("Recall: %.4f", recall)
            logger.info("F1 Score: %.4f", f1)
            logger.info("Confusion Matrix:\n%s", conf_matrix)
            
            # Save the model and scaler
            self.save_model()
            
            self.training_status = "completed"
            self.training_error = None
            logger.info("Training process completed successfully")
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            self.training_status = "error"
            self.training_error = str(e)
            raise

    def save_model(self):
        """Save the trained model and scaler."""
        try:
            joblib.dump(self.model, MODEL_PATH)
            joblib.dump(self.scaler, SCALER_PATH)
            logger.info(f"Model and scaler saved to {MODEL_PATH} and {SCALER_PATH}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def load_model(self):
        """Load the trained model and scaler."""
        try:
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            logger.info("Model and scaler loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, features):
        """Make predictions using the trained model."""
        try:
            if self.model is None:
                self.load_model()
            
            # Scale the features
            features_scaled = self.scaler.transform([features])
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            return prediction
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise

    def get_status(self):
        """Get the current status of the training process."""
        return {
            "status": self.training_status,
            "last_training_time": self.last_training_time.isoformat() if self.last_training_time else None,
            "error": self.training_error,
            "metrics": self.model_metrics
        }