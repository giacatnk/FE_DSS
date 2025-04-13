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
    
    @action(detail=False, methods=['delete'])
    def delete_patient(self, request):
        """Delete a patient by ID"""
        patient_id = request.query_params.get('id', None)
        if not patient_id:
            return Response(
                {'error': 'Patient ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.delete()
            return Response(
                {'message': f'Patient {patient_id} deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Patient.DoesNotExist:
            return Response(
                {'error': f'Patient with ID {patient_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get_queryset(self):
        queryset = Patient.objects.all()
        page = self.request.query_params.get('page', None)
        offset = self.request.query_params.get('offset', None)

        if page is not None and offset is not None:
            try:
                page = int(page)
                offset = int(offset)
                start = (page - 1) * offset
                end = start + offset
                queryset = queryset[start:end]
            except ValueError:
                pass
        return queryset
        
    def destroy(self, request, *args, **kwargs):
        """Override destroy to handle custom logic when deleting a patient"""
        instance = self.get_object()
        patient_id = instance.id
        
        # Delete all related alerts first
        Alert.objects.filter(patient_id=patient_id).delete()
        
        # Delete the patient
        self.perform_destroy(instance)
        
        return Response(
            {'message': f'Patient {patient_id} and all related alerts deleted successfully'},
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        """Override create to make prediction after patient creation"""
        # First create the patient
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        patient = serializer.instance
        
        # Make prediction for the new patient
        prediction_result = predict_batch([patient.id])
        
        if 'predictions' in prediction_result and prediction_result['predictions']:
            # Get the prediction result
            prediction = prediction_result['predictions'][0]
            
            # Create alert
            alert = Alert.objects.create(
                patient_id=patient.id,
                prediction=bool(prediction['prediction'] >= 0.5),
                confidence=float(prediction['prediction']),
                model_version='1.1'  # get_model_status().get('version', 'unknown')
            )
            
            print(f"Created alert {alert.id} for patient {patient.id}")
            
            # Now serialize the patient again to include the latest alert
            patient = Patient.objects.get(id=patient.id)  # Refresh from database
            patient_serializer = PatientSerializer(patient)
            
            # Create the response
            headers = self.get_success_headers(serializer.data)
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        # If no prediction was made, return the original response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Override update to make new prediction after patient update"""
        partial = kwargs.pop('partial', True)  # Set to True for partial updates
        instance = self.get_object()
        
        # Get the current patient data
        current_data = PatientSerializer(instance).data
        
        # Update only the provided fields
        updated_data = {**current_data, **request.data}
        
        # Remove any fields that were not provided in the request
        for field in current_data.keys():
            if field not in request.data:
                updated_data.pop(field, None)
        
        serializer = self.get_serializer(instance, data=updated_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Make new prediction for the updated patient
        prediction_result = predict_batch([instance.id])
        
        if 'predictions' in prediction_result and prediction_result['predictions']:
            # Get the prediction result
            prediction = prediction_result['predictions'][0]
            
            # Create new alert
            alert = Alert.objects.create(
                patient_id=instance.id,
                prediction=bool(prediction['prediction'] >= 0.5),
                confidence=float(prediction['prediction']),
                model_version='1.1'  # get_model_status().get('version', 'unknown')
            )
            
            print(f"Created new alert {alert.id} for updated patient {instance.id}")
            
            # Now serialize the patient again to include the latest alert
            patient = Patient.objects.get(id=instance.id)  # Refresh from database
            patient_serializer = PatientSerializer(patient)
            
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

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
