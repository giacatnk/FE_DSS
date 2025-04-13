import requests
import json
from datetime import datetime
from ..models import Patient, Alert

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
    alerts = Alert.objects.filter(is_correct__isnull=False)
    
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
        
        response = requests.post('http://localhost:8080/retrain', json=training_data)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def predict_batch(patient_ids):
    """Make predictions for multiple patients using the ML service"""
    try:
        # Get features for all patients
        patients = Patient.objects.filter(id__in=patient_ids)
        features_list = []
        
        for patient in patients:
            features_list.append(get_features_from_patient(patient))
        
        # Send batch prediction request to ML service
        response = requests.post(
            'http://localhost:8080/predict',
            json={'patients': features_list}
        )
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def get_model_status():
    """Get current model status from ML service"""
    try:
        response = requests.get('http://localhost:8080/status')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}