from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from diabetes_predictor.models import Patient, Alert
from datetime import datetime

class BaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_data = {
            "name": "John Doe",
            "admission_date": datetime.now().isoformat(),
            "age": 45.0,
            "weight": 75.0,
            "gender": "M",
            "platelets": 250000.0,
            "spo2": 98.0,
            "creatinine": 0.9,
            "hematocrit": 45.0,
            "aids": 0,
            "lymphoma": 0,
            "solid_tumor_with_metastasis": 0,
            "heartrate": 75.0,
            "calcium": 2.5,
            "wbc": 7.0,
            "glucose": 100.0,
            "inr": 1.1,
            "potassium": 4.0,
            "sodium": 140.0,
            "ethnicity": 1
        }
        self.patient = Patient.objects.create(**self.patient_data)
        self.alert = Alert.objects.create(
            patient=self.patient,
            prediction=True,
            confidence=0.85,
            model_version="v1.0"
        )

class TestUrls:
    PATIENTS = reverse('patient-list')
    ALERTS = reverse('alert-list')
    MODEL_STATUS = reverse('model-status')
    MODEL_RETRAIN = reverse('model-retrain')
    
    @staticmethod
    def patient_detail(pk):
        return reverse('patient-detail', args=[pk])
    
    @staticmethod
    def alert_detail(pk):
        return reverse('alert-detail', args=[pk])
    
    @staticmethod
    def alert_label(pk):
        return reverse('alert-label', args=[pk])
    
    @staticmethod
    def model_predict():
        return reverse('model-predict')
