from rest_framework import serializers
from .models import Patient, Alert

class AlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    
    class Meta:
        model = Alert
        fields = ['id', 'patient', 'patient_name', 'prediction', 'confidence', 'model_version', 'is_correct', 'created_at']

class PatientSerializer(serializers.ModelSerializer):
    latest_alert = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
    
    def get_latest_alert(self, obj):
        """Get the latest alert for this patient"""
        try:
            # Print for debugging
            # print(f"Getting latest alert for patient {obj.id}")
            # Use direct ORM query to find alerts for this patient
            alerts = Alert.objects.filter(patient_id=obj.id).order_by('-created_at')
            
            if alerts.exists():
                alert = alerts.first()
                print(f"Found alert: {alert.id}")
                serializer = AlertSerializer(alert)
                return serializer.data
            else:
                print(f"No alerts found for patient {obj.id}")
                return None
        except Exception as e:
            print(f"Error getting latest alert: {str(e)}")
            return None