import pandas as pd
import random
from datetime import datetime, timedelta
import names
from diabetes_predictor.models import Patient, Alert
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import data from CSV and create patients with random names and admission dates'

    def handle(self, *args, **options):
        # Read the CSV file
        df = pd.read_csv('data/mock.csv')
        
        # Get first 1000 rows
        df = df.head(10)
        
        # Generate random admission dates between 2022-01-01 and 2022-12-31
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 12, 31)
        
        total_rows = len(df)
        
        # Create a list of model versions for different time periods
        model_versions = [
            "20220115_143000",  # January
            "20220420_101500",  # April
            "20220715_164500",  # July
            "20221025_113000",  # October
            "20221231_094500"   # December
        ]
        
        for index, row in df.iterrows():
            # Generate random admission date
            random_days = random.randint(0, (end_date - start_date).days)
            admission_date = start_date + timedelta(days=random_days)
            
            # Generate random name
            gender = 'M' if random.random() > 0.5 else 'F'
            name = names.get_full_name(gender='male' if gender == 'M' else 'female')
            
            # Create patient
            patient = Patient(
                name=name,
                admission_date=admission_date,
                age=float(row['age']),
                weight=float(row['weight']),
                gender=gender,
                platelets=float(row['platelets']),
                spo2=float(row['spo2']),
                creatinine=float(row['creatinine']),
                hematocrit=float(row['hematocrit']),
                aids=int(row['aids']),
                lymphoma=int(row['lymphoma']),
                solid_tumor_with_metastasis=int(row['solid_tumor_with_metastasis']),
                heartrate=float(row['heartrate']),
                calcium=float(row['calcium']),
                wbc=float(row['wbc']),
                glucose=float(row['glucose']),
                inr=float(row['inr']),
                potassium=float(row['potassium']),
                sodium=float(row['sodium']),
                ethnicity=int(row['ethnicity'])
            )
            patient.save()
            
            # Create alert for the patient
            # Determine which model version to use based on admission date
            model_version = None
            for version in model_versions:
                version_date = datetime.strptime(version[:8], "%Y%m%d")
                if admission_date <= version_date:
                    model_version = version
                    break
            if not model_version:
                model_version = model_versions[-1]  # Use the latest version
            
            # Generate prediction based on the mock data
            # We'll use the diabetes column as our ground truth
            is_diabetes = False if random.random() < 0.5 else True
            
            # Add some randomness to the prediction
            prediction = is_diabetes
            if random.random() < 0.1:  # 10% chance of incorrect prediction
                prediction = not prediction
            
            # Generate confidence score
            confidence = random.uniform(0.6, 0.95) if prediction == is_diabetes else random.uniform(0.4, 0.8)
            
            # Create alert
            alert = Alert(
                patient=patient,
                prediction=prediction,
                confidence=confidence,
                is_correct=None,  # Start with no labels
                model_version=model_version
            )
            alert.save()
            
            # Print progress
            if (index + 1) % 100 == 0:
                self.stdout.write(f'Processed {index + 1} out of {total_rows} patients')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {total_rows} patients and alerts'))
