from django.test import TestCase
from unittest.mock import patch, Mock
from diabetes_predictor.models import Patient
from diabetes_predictor.ml_models.diabetes_model import predict_batch, retrain, get_model_status
from datetime import datetime

class MLModelTest(TestCase):
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

    @patch('requests.post')
    def test_predict_batch(self, mock_post):
        """Test batch prediction with mock ML service"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'predictions': [{'prediction': 0.85}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = predict_batch([self.patient.id])
        
        self.assertTrue('predictions' in result)
        self.assertEqual(len(result['predictions']), 1)
        self.assertTrue('prediction' in result['predictions'][0])

    @patch('requests.post')
    def test_retrain(self, mock_post):
        """Test model retraining with mock ML service"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'success',
            'message': 'Model retrained successfully'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = retrain()
        
        self.assertTrue('status' in result)
        self.assertEqual(result['status'], 'success')

    @patch('requests.get')
    def test_get_model_status(self, mock_get):
        """Test getting model status with mock ML service"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'ready',
            'version': 'v1.0',
            'accuracy': 0.95
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_model_status()
        
        self.assertTrue('status' in result)
        self.assertEqual(result['status'], 'ready')
        self.assertTrue('version' in result)

    def test_get_features_from_patient(self):
        """Test feature extraction from patient"""
        from diabetes_predictor.ml_models.diabetes_model import get_features_from_patient
        
        features = get_features_from_patient(self.patient)
        
        self.assertTrue('age' in features)
        self.assertTrue('weight' in features)
        self.assertTrue('gender' in features)
        self.assertTrue('platelets' in features)
        self.assertEqual(len(features), 18)  # Verify all features are present
