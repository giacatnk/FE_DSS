from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from diabetes_predictor.models import Patient, Alert
from datetime import datetime
from .test_setup import BaseTest, TestUrls

class PatientViewSetTest(BaseTest):
    def setUp(self):
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

    def test_create_patient(self):
        """Test creating a new patient"""
        response = self.client.post(TestUrls.PATIENTS, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
        self.assertTrue('latest_alert' in response.data)
        self.assertIsNotNone(response.data['latest_alert'])
        self.assertTrue('prediction' in response.data['latest_alert'])
        self.assertTrue('confidence' in response.data['latest_alert'])
        
    def test_list_patients(self):
        """Test listing all patients"""
        response = self.client.get(TestUrls.PATIENTS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        
    def test_retrieve_patient(self):
        """Test retrieving a specific patient"""
        patient = Patient.objects.create(**self.patient_data)
        response = self.client.get(TestUrls.patient_detail(patient.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.patient_data['name'])
        self.assertTrue('latest_alert' in response.data)
        if response.data['latest_alert']:
            self.assertEqual(response.data['latest_alert']['patient'], patient.id)

class AlertViewSetTest(BaseTest):
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Jane Smith",
            admission_date=datetime.now(),
            age=50.0,
            weight=65.0,
            gender="F",
            platelets=200000.0,
            spo2=95.0,
            creatinine=1.2,
            hematocrit=40.0,
            aids=0,
            lymphoma=0,
            solid_tumor_with_metastasis=0,
            heartrate=70.0,
            calcium=2.4,
            wbc=6.0,
            glucose=95.0,
            inr=1.0,
            potassium=3.8,
            sodium=138.0,
            ethnicity=1
        )
        self.alert = Alert.objects.create(
            patient=self.patient,
            prediction=True,
            confidence=0.85,
            model_version="v1.0"
        )

    def test_list_alerts(self):
        """Test listing all alerts"""
        response = self.client.get(TestUrls.ALERTS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_alert(self):
        """Test retrieving a specific alert"""
        response = self.client.get(TestUrls.alert_detail(self.alert.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['prediction'], True)

    def test_label_alert(self):
        """Test labeling an alert"""
        response = self.client.post(
            TestUrls.alert_label(self.alert.id),
            {'is_correct': True},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_correct'])

class ModelViewSetTest(BaseTest):
    def setUp(self):
        self.patient = Patient.objects.create(
            name="Test Patient",
            admission_date=datetime.now(),
            age=40.0,
            weight=70.0,
            gender="M",
            platelets=220000.0,
            spo2=97.0,
            creatinine=1.0,
            hematocrit=42.0,
            aids=0,
            lymphoma=0,
            solid_tumor_with_metastasis=0,
            heartrate=72.0,
            calcium=2.45,
            wbc=6.5,
            glucose=98.0,
            inr=1.05,
            potassium=4.1,
            sodium=139.0,
            ethnicity=1
        )

    def test_predict(self):
        """Test batch prediction"""
        response = self.client.post(
            TestUrls.model_predict(),
            {'patient_ids': [self.patient.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('predictions' in response.data)
        self.assertEqual(len(response.data['predictions']), 1)
        prediction = response.data['predictions'][0]
        self.assertTrue('prediction' in prediction)
        self.assertTrue('confidence' in prediction)

    def test_retrain(self):
        """Test model retraining"""
        response = self.client.post(TestUrls.MODEL_RETRAIN, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('status' in response.data)
        self.assertEqual(response.data['status'], 'success')
