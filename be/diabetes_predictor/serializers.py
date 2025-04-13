from rest_framework import serializers
from .models import Patient, Alert
from typing import List, Dict, Any

class PredictionPatientSerializer(serializers.ModelSerializer):
    gender_M = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'age',
            'weight',
            'gender_M',
            'platelets',
            'spo2',
            'creatinine',
            'hematocrit',
            'aids',
            'lymphoma',
            'solid_tumor_with_metastasis',
            'heartrate',
            'calcium',
            'wbc',
            'glucose',
            'inr',
            'potassium',
            'sodium',
            'ethnicity'
        ]

    def get_gender_M(self, obj: Patient) -> int:
        """Convert gender to binary format where M=1, others=0"""
        return 1 if obj.gender == 'M' else 0

class PatientSerializer(serializers.ModelSerializer):
    latest_alert = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_latest_alert(self, obj: Patient) -> Dict[str, Any]:
        try:
            alert = Alert.objects.filter(patient_id=obj.id).latest('created_at')
            return AlertSerializer(alert).data
        except Alert.DoesNotExist:
            return None

    def to_representation(self, instance: Patient) -> Dict[str, Any]:
        """Convert patient to dictionary format for prediction"""
        ret = super().to_representation(instance)
        # ret['prediction_data'] = PredictionPatientSerializer(instance).data
        return ret

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['created_at']