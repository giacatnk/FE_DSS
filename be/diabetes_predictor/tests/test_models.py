from django.test import TestCase
from diabetes_predictor.models import Patient, Alert
from datetime import datetime
from .test_setup import BaseTest

class PatientModelTest(BaseTest):
    def setUp(self):
        self.patient = Patient.objects.create(
            name="John Doe",
            admission_date=datetime.now(),
            age=45.0,
            weight=75.0,
            gender="M",
            platelets=250000.0,
            spo2=98.0,
            creatinine=0.9,
            hematocrit=45.0,
            aids=0,
            lymphoma=0,
            solid_tumor_with_metastasis=0,
            heartrate=75.0,
            calcium=2.5,
            wbc=7.0,
            glucose=100.0,
            inr=1.1,
            potassium=4.0,
            sodium=140.0,
            ethnicity=1
        )

    def test_patient_creation(self):
        """Test patient creation"""
        self.assertTrue(isinstance(self.patient, Patient))
        self.assertEqual(self.patient.name, "John Doe")
        self.assertEqual(self.patient.age, 45.0)

    def test_patient_string_representation(self):
        """Test patient string representation"""
        self.assertEqual(str(self.patient), "Patient {} - Age: {}, Gender: M".format(self.patient.id, 45.0))

class AlertModelTest(BaseTest):
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

    def test_alert_creation(self):
        """Test alert creation"""
        self.assertTrue(isinstance(self.alert, Alert))
        self.assertEqual(self.alert.prediction, True)
        self.assertEqual(self.alert.confidence, 0.85)

    def test_alert_string_representation(self):
        """Test alert string representation"""
        self.assertEqual(str(self.alert), "Alert for {}: Positive".format(self.patient.id))

    def test_alert_update(self):
        """Test updating alert with is_correct"""
        self.alert.is_correct = True
        self.alert.save()
        self.assertTrue(self.alert.is_correct)

    def test_alert_model_version(self):
        """Test model version field"""
        self.assertEqual(self.alert.model_version, "v1.0")
