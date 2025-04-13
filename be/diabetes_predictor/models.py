from django.db import models
from typing import Dict, Any

class Patient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    admission_date = models.DateTimeField(null=True, blank=True)
    age = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10)
    platelets = models.FloatField()
    spo2 = models.FloatField()
    creatinine = models.FloatField()
    hematocrit = models.FloatField()
    aids = models.IntegerField()
    lymphoma = models.IntegerField()
    solid_tumor_with_metastasis = models.IntegerField()
    heartrate = models.FloatField()
    calcium = models.FloatField()
    wbc = models.FloatField()
    glucose = models.FloatField()
    inr = models.FloatField()
    potassium = models.FloatField()
    sodium = models.FloatField()
    ethnicity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert patient to dictionary format for prediction"""
        return {
            "age": float(self.age),
            "weight": float(self.weight),
            "gender_M": 1 if self.gender == 'M' else 0,
            "platelets": float(self.platelets),
            "spo2": float(self.spo2),
            "creatinine": float(self.creatinine),
            "hematocrit": float(self.hematocrit),
            "aids": int(self.aids),
            "lymphoma": int(self.lymphoma),
            "solid_tumor_with_metastasis": int(self.solid_tumor_with_metastasis),
            "heartrate": float(self.heartrate),
            "calcium": float(self.calcium),
            "wbc": float(self.wbc),
            "glucose": float(self.glucose),
            "inr": float(self.inr),
            "potassium": float(self.potassium),
            "sodium": float(self.sodium),
            "ethnicity": int(self.ethnicity)
        }

class Alert(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    prediction = models.BooleanField(default=False)
    confidence = models.FloatField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, default=True)
    model_version = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.patient.id}: {'Positive' if self.prediction else 'Negative'}"