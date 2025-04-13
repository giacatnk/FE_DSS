from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    admission_date = models.DateTimeField(null=True, blank=True)
    age = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
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
        return f"Patient {self.id} - Age: {self.age}, Gender: {self.gender}"

class Alert(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    prediction = models.BooleanField(default=False)
    confidence = models.FloatField()
    is_correct = models.BooleanField(null=True)
    model_version = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Alert for {self.patient.id}: {'Positive' if self.prediction else 'Negative'}"