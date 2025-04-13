from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Alert
from .serializers import PatientSerializer, AlertSerializer, PredictionPatientSerializer
from .ml_models.diabetes_model import predict_batch, retrain, get_model_status
from .utils import parse_jdbc_url, convert_patient_data
from django.shortcuts import get_object_or_404
from typing import List, Dict, Any
from django.db import transaction
import psycopg2
from datetime import datetime
from django.utils import timezone
from urllib.parse import urlparse
import random
import logging

logger = logging.getLogger(__name__)

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing patients
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    @action(detail=False, methods=['delete'])
    def delete_patient(self, request) -> Response:
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

    def get_queryset(self) -> List[Patient]:
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
        
    def destroy(self, request, *args, **kwargs) -> Response:
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
    
    def create(self, request, *args, **kwargs) -> Response:
        """Override create to make prediction after patient creation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Make new prediction for the created patient
        prediction_result = predict_batch([PredictionPatientSerializer(serializer.instance).data])
        
        if 'predictions' in prediction_result and prediction_result['predictions']:
            # Get the prediction result
            prediction = prediction_result['predictions'][0]
            
            # Create new alert
            alert = Alert.objects.create(
                patient_id=serializer.instance.id,
                prediction=bool(prediction['prediction'] >= 0.5),
                confidence=None,#float(prediction['prediction']),
                model_version='1.1'  # get_model_status().get('version', 'unknown')
            )
            
            print(f"Created new alert {alert.id} for patient {serializer.instance.id}")
            
            # Now serialize the patient again to include the latest alert
            patient = Patient.objects.get(id=serializer.instance.id)  # Refresh from database
            patient_serializer = PatientSerializer(patient)
            
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        """Override update to make new prediction after patient update"""
        partial = kwargs.pop('partial', True)  # Set to True for partial updates
        instance = self.get_object()
        
        # Get the current patient data
        current_data = PredictionPatientSerializer(instance).data
        
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
        prediction_result = predict_batch([PredictionPatientSerializer(serializer.instance).data])
        
        if 'predictions' in prediction_result and prediction_result['predictions']:
            # Get the prediction result
            prediction = prediction_result['predictions'][0]
            
            # Create new alert
            alert = Alert.objects.create(
                patient=instance,
                prediction=prediction['prediction'],
                confidence=prediction.get('confidence', None),
                model_version='1.1'  # get_model_status().get('version', 'unknown')
            )
            
            print(f"Created new alert {alert.id} for updated patient {instance.id}")
            
            # Now serialize the patient again to include the latest alert
            patient = Patient.objects.get(id=instance.id)  # Refresh from database
            patient_serializer = PatientSerializer(patient)
            
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def predict(self, request) -> Response:
        """Make predictions for multiple patients"""
        patient_ids = request.data.get('patient_ids', [])
        if not patient_ids:
            return Response({
                'error': 'No patient IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get patient data from database
        patients = Patient.objects.filter(id__in=patient_ids)
        if not patients:
            return Response({
                'error': 'No patients found with the provided IDs'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get prediction data for each patient
        patient_data = [PredictionPatientSerializer(patient).data for patient in patients]
        
        # Make prediction with serialized data
        result = predict_batch(patient_data)
        
        # Transform the response to match our format
        predictions = []
        if 'predictions' in result:
            for pred in result['predictions']:
                predictions.append({
                    'prediction': pred['prediction'],
                    'confidence': None
                })
        
        return Response({
            'predictions': predictions,
            'model_version': result.get('model_version', 'unknown'),
            'status': 'success' if 'predictions' in result else 'error'
        })

    @action(detail=False, methods=['get'], url_path='sync')
    def sync_patients(self, request):
        """
        Sync patients from source database to web database.
        
        Parameters:
        - start_time: Optional. Defaults to latest enrollment date in web database.
        - end_time: Optional. Defaults to current time.
        - source_db_url: Optional. Defaults to "jdbc:postgresql://localhost:5432/source_db".
        
        Returns:
        - List of synced patients with their alerts.
        - Total number of patients synced.
        """
        try:
            # Get latest enrollment date from web database
            latest_patient = Patient.objects.order_by('-admission_date').first()
            start_time = latest_patient.admission_date if latest_patient else datetime(2022, 1, 1)
            logger.info(f"Start time: {start_time}")
            # print(f"Start time: {start_time}")
            # Get current time for end_time
            end_time = timezone.now()
            logger.info(f"End time: {end_time}")
            
            # Default source database connection
            source_db_url = "jdbc:postgresql://localhost:5432/source_db"
            logger.info(f"Source DB URL: {source_db_url}")
            
            # Parse source database URL
            conn_params = parse_jdbc_url(source_db_url)
            logger.info(f"Connection params: {conn_params}")
            
            # Connect to source database
            source_conn = psycopg2.connect(
                dbname=conn_params['dbname'],
                user=conn_params['user'],
                password=conn_params['password'],
                host=conn_params['host'],
                port=conn_params['port']
            )
            logger.info("Connected to source database")
            
            # Create cursor for source database
            source_cursor = source_conn.cursor()
            
            # Build query with time range filter
            query = """
                SELECT * FROM patients
                WHERE admission_date >= %s AND admission_date <= %s
                ORDER BY admission_date
                LIMIT 10
            """
            logger.info(f"Executing query: {query}")
            
            # Execute query with parameters
            source_cursor.execute(query, (start_time, end_time))
            source_patients = source_cursor.fetchall()
            source_columns = [desc[0] for desc in source_cursor.description]
            logger.info(f"Found {len(source_patients)} patients to sync")
            
            # Transaction to ensure atomicity
            with transaction.atomic():
                synced_patients = []
                
                for patient in source_patients:
                    patient_dict = dict(zip(source_columns, patient))
                    logger.info(f"Processing patient: {patient_dict['name']}")
                    
                    # Convert types
                    patient_dict = convert_patient_data(patient_dict)
                    logger.info(f"Converted patient data: {patient_dict}")
                    
                    # Create patient
                    patient_instance = Patient.objects.create(**patient_dict)
                    logger.info(f"Created patient with ID: {patient_instance.id}")
                    
                    # Serialize patient data for prediction
                    serialized_patient = PredictionPatientSerializer(patient_instance).data
                    logger.info(f"Serialized patient data: {serialized_patient}")
                    
                    # Create alert
                    prediction = predict_batch([serialized_patient])['predictions'][0]['prediction']
                    confidence = random.uniform(0.6, 0.95)
                    logger.info(f"Prediction result: {prediction}, Confidence: {confidence}")
                    
                    alert = Alert.objects.create(
                        patient=patient_instance,
                        prediction=prediction,
                        confidence=confidence,
                        model_version="latest"
                    )
                    logger.info(f"Created alert with ID: {alert.id}")
                    
                    # Prepare response data
                    synced_patients.append({
                        "id": patient_instance.id,
                        "name": patient_instance.name,
                        "admission_date": patient_instance.admission_date,
                        "latest_alert": AlertSerializer(alert).data
                    })
                
                logger.info(f"Total synced patients: {len(synced_patients)}")
                logger.info(f"Synced patients data: {synced_patients}")
            
            response_data = {
                "patients": synced_patients,
                "total_synced": len(synced_patients)
            }
            logger.info(f"Final response data: {response_data}")
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in sync_patients: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        finally:
            if 'source_cursor' in locals():
                source_cursor.close()
            if 'source_conn' in locals():
                source_conn.close()

class AlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing alerts
    """
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer
    
    @action(detail=True, methods=['post'])
    def label(self, request, pk=None) -> Response:
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
    def retrain(self, request) -> Response:
        """Retrain the model with the latest data"""
        result = retrain()
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def status(self, request) -> Response:
        """Get current model status"""
        result = get_model_status()
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def predict(self, request) -> Response:
        """Make predictions for multiple patients"""
        patient_ids = request.data.get('patient_ids', [])
        if not patient_ids:
            return Response({
                'error': 'No patient IDs provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get patient data from database
        patients = Patient.objects.filter(id__in=patient_ids)
        if not patients:
            return Response({
                'error': 'No patients found with the provided IDs'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get prediction data for each patient
        patient_data = [PredictionPatientSerializer(patient).data for patient in patients]
        
        # Make prediction with serialized data
        result = predict_batch(patient_data)
        
        # Transform the response to match our format
        predictions = []
        if 'predictions' in result:
            for pred in result['predictions']:
                predictions.append({
                    'prediction': pred['prediction'],
                    'confidence': None#pred['confidence']
                })
        
        return Response({
            'predictions': predictions,
            'model_version': result.get('model_version', 'unknown'),
            'status': 'success' if 'predictions' in result else 'error'
        })
