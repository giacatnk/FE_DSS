from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Alert
from .serializers import PatientSerializer, AlertSerializer
from .ml_models.diabetes_model import predict_batch, retrain, get_model_status

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing patients
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to make prediction after patient creation"""
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            # Make prediction for the new patient
            patient_id = response.data['id']
            prediction_result = predict_batch([patient_id])
            
            # Add prediction info to response
            if 'predictions' in prediction_result and prediction_result['predictions']:
                prediction = prediction_result['predictions'][0]
                response.data['prediction'] = {
                    'prediction': prediction['prediction'] >= 0.5,
                    'confidence': prediction['prediction']
                }
            
        return response

class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing alerts
    """
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer
    
    @action(detail=True, methods=['post'])
    def label(self, request, pk=None):
        """Label an alert as correct or incorrect"""
        alert = self.get_object()
        
        # Get the label data from request
        is_correct = request.data.get('is_correct', None)
        if is_correct is None:
            return Response(
                {'error': 'is_correct field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the alert
        alert.is_correct = is_correct
        alert.save()
        
        # Return the updated alert
        serializer = self.get_serializer(alert)
        return Response(serializer.data)

class ModelViewSet(viewsets.ViewSet):
    """
    API endpoint for model operations
    """
    
    @action(detail=False, methods=['post'])
    def retrain(self, request):
        """Retrain the model with the latest data"""
        result = retrain()
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Get current model status"""
        result = get_model_status()
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Make predictions for multiple patients"""
        patient_ids = request.data.get('patient_ids', [])
        if not patient_ids:
            return Response({
                'error': 'No patient IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = predict_batch(patient_ids)
        
        # Transform the response to match our format
        predictions = []
        if 'predictions' in result:
            for pred in result['predictions']:
                predictions.append({
                    'prediction': pred['prediction'] >= 0.5,
                    'confidence': pred['prediction']
                })
        
        return Response({'predictions': predictions})
