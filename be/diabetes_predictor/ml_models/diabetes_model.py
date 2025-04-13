import os
import logging
import json
import random
import requests
from datetime import datetime
from ..models import Patient, Alert
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Get ML service URL from environment variable or use default
ML_SERVICE_URL = os.getenv('ML_API_URL', 'http://localhost:8080')

def get_features_from_patient(patient):
    """Extract features from a patient object"""
    return {
        "age": float(patient.age),
        "weight": float(patient.weight),
        "gender": patient.gender,
        "platelets": float(patient.platelets),
        "spo2": float(patient.spo2),
        "creatinine": float(patient.creatinine),
        "hematocrit": float(patient.hematocrit),
        "aids": int(patient.aids),
        "lymphoma": int(patient.lymphoma),
        "solid_tumor_with_metastasis": int(patient.solid_tumor_with_metastasis),
        "heartrate": float(patient.heartrate),
        "calcium": float(patient.calcium),
        "wbc": float(patient.wbc),
        "glucose": float(patient.glucose),
        "inr": float(patient.inr),
        "potassium": float(patient.potassium),
        "sodium": float(patient.sodium),
        "ethnicity": int(patient.ethnicity)
    }

def get_training_data():
    """Get training data from patients and labeled alerts"""
    # Get patients with labeled alerts
    alerts = Alert.objects.all()#.filter(is_correct=True)
    
    features = []
    labels = []
    
    for alert in alerts:
        patient = alert.patient
        features.append(get_features_from_patient(patient))
        # Use the labeled value (is_correct) if the prediction was correct
        # otherwise use opposite of the prediction
        if alert.is_correct:
            labels.append(alert.prediction)
        else:
            labels.append(not alert.prediction)
    
    return features, labels

def retrain():
    """Retrain the model using the ML service"""
    try:
        # Get training data
        features, labels = get_training_data()
        
        if len(features) < 10:  # Not enough data to train
            return {
                'status': 'error',
                'message': 'Not enough labeled data to train (minimum 10 required)'
            }
        
        # Send training request to ML service
        training_data = {
            'features': features,
            'labels': labels
        }
        
        response = requests.post(
            f'{ML_SERVICE_URL}/retrain',
            json=training_data,
            # timeout=10  # Add timeout
        )
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        return {
            'status': 'error',
            'message': f'Failed to connect to ML service: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error in retrain: {str(e)}")
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }

def predict_batch(patient_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Predict diabetes risk for a batch of patients using serialized patient data
    
    Args:
        patient_data: List of serialized patient data in JSON format
        
    Returns:
        Dict containing predictions for each patient
        {
            "predictions": [
                {
                    "prediction": 0.0,
                    "confidence": null
                }
            ],
            "model_version": "unknown",
            "status": "success"
        }
    """
    try:
        if not patient_data:
            return {'error': 'No patient data provided'}
        # print('hehehe', patient_data)
        # Send batch prediction request to ML service
        response = requests.post(
            f'{ML_SERVICE_URL}/predict',
            json={'patients': patient_data},
            timeout=10  # Add timeout
        )
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to ML service: {str(e)}")
        return {'error': f'Failed to connect to ML service: {str(e)}'}
    except Exception as e:
        logger.error(f"Unexpected error in predict_batch: {str(e)}")
        return {'error': f'Unexpected error: {str(e)}'}

def get_model_status() -> Dict[str, Any]:
    """Get current model status from ML service
    
    Returns:
        Dict with model status information
    """
    try:
        response = requests.get(
            f'{ML_SERVICE_URL}/status',
            timeout=5  # Add timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting model status: {str(e)}")
        return {'error': f'Failed to get model status: {str(e)}', 'status': 'unavailable'}
    except Exception as e:
        logger.error(f"Unexpected error in get_model_status: {str(e)}")
        return {'error': f'Unexpected error: {str(e)}', 'status': 'error'}