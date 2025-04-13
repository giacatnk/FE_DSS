from rest_framework import serializers
from .models import Patient, Alert

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    
    class Meta:
        model = Alert
        fields = ['id', 'patient', 'patient_name', 'prediction', 'confidence', 'model_version', 'is_correct', 'created_at']