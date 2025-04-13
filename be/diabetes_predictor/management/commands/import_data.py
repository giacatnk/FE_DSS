from django.core.management.base import BaseCommand
from django.db import transaction
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
from diabetes_predictor.utils import parse_jdbc_url
import psycopg2

class Command(BaseCommand):
    help = 'Sync the first 100 patients from source database to web database'

    def handle(self, *args, **options):
        try:
            # Default database and API URLs
            source_db_url = 'jdbc:postgresql://localhost:5432/source_db'
            api_url = 'http://localhost:8000/api/patients/'
            
            # Connect to source database
            conn_params = parse_jdbc_url(source_db_url)
            source_conn = psycopg2.connect(**conn_params)
            source_cursor = source_conn.cursor()

            # Get first 100 patients from source database
            source_cursor.execute("""
                SELECT * FROM patients
                ORDER BY admission_date
                LIMIT 100
            """)

            source_patients = source_cursor.fetchall()
            source_columns = [desc[0] for desc in source_cursor.description]

            synced_patients = 0

            # Sync patients using the API
            for patient in source_patients:
                patient_dict = dict(zip(source_columns, patient))
                
                # Prepare the request body
                request_data = {
                    'name': patient_dict['name'],
                    'admission_date': patient_dict['admission_date'].isoformat(),
                    'age': float(patient_dict['age']),
                    'weight': float(patient_dict['weight']),
                    'gender': patient_dict['gender'],
                    'platelets': float(patient_dict['platelets']),
                    'spo2': float(patient_dict['spo2']),
                    'creatinine': float(patient_dict['creatinine']),
                    'hematocrit': float(patient_dict['hematocrit']),
                    'aids': int(patient_dict['aids']),
                    'lymphoma': int(patient_dict['lymphoma']),
                    'solid_tumor_with_metastasis': int(patient_dict['solid_tumor_with_metastasis']),
                    'heartrate': float(patient_dict['heartrate']),
                    'calcium': float(patient_dict['calcium']),
                    'wbc': float(patient_dict['wbc']),
                    'glucose': float(patient_dict['glucose']),
                    'inr': float(patient_dict['inr']),
                    'potassium': float(patient_dict['potassium']),
                    'sodium': float(patient_dict['sodium']),
                    'ethnicity': int(patient_dict['ethnicity'])
                }

                # Make POST request to create patient
                response = requests.post(
                    api_url,
                    json=request_data,
                    headers={'Content-Type': 'application/json'}
                )

                if response.status_code == 201:
                    synced_patients += 1
                else:
                    self.stdout.write(self.style.ERROR(
                        f"Failed to sync patient {patient_dict['name']}: {response.text}"
                    ))

            self.stdout.write(self.style.SUCCESS(
                f'Successfully synced {synced_patients} out of 100 patients'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise
        finally:
            if 'source_cursor' in locals():
                source_cursor.close()
            if 'source_conn' in locals():
                source_conn.close()
