from django.core.management.base import BaseCommand
import pandas as pd
from psycopg2.extras import execute_values
from django.db import connection
from django.db.utils import IntegrityError
from datetime import datetime, timedelta
import names
import random
import os
from urllib.parse import urlparse
from diabetes_predictor.utils import parse_jdbc_url
import psycopg2

class Command(BaseCommand):
    help = 'Initialize source database with patient data and clear web database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source_db_url',
            type=str,
            default='jdbc:postgresql://localhost:5432/source_db',
            help='JDBC URL for the source database'
        )

    def handle(self, *args, **options):
        try:
            # Parse source database URL
            source_db_url = options['source_db_url']
            
            # Connect to source database
            conn_params = parse_jdbc_url(source_db_url)
            source_conn = psycopg2.connect(**conn_params)
            
            # Create cursor for source database
            source_cursor = source_conn.cursor()
            
            # Create patients table in source database
            source_cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    admission_date TIMESTAMP,
                    age FLOAT,
                    weight FLOAT,
                    gender VARCHAR(10),
                    platelets FLOAT,
                    spo2 FLOAT,
                    creatinine FLOAT,
                    hematocrit FLOAT,
                    aids INTEGER,
                    lymphoma INTEGER,
                    solid_tumor_with_metastasis INTEGER,
                    heartrate FLOAT,
                    calcium FLOAT,
                    wbc FLOAT,
                    glucose FLOAT,
                    inr FLOAT,
                    potassium FLOAT,
                    sodium FLOAT,
                    ethnicity INTEGER
                );
            """)
            
            # Read the CSV file
            df = pd.read_csv('data/mock.csv').head(1000)
            
            # Prepare data for insertion
            values = []
            for index, row in df.iterrows():
                # Generate random admission date
                start_date = datetime(2022, 1, 1)
                end_date = datetime(2022, 12, 31)
                random_days = random.randint(0, (end_date - start_date).days)
                admission_date = start_date + timedelta(days=random_days)
                
                # Generate random name
                gender = 'M' if random.random() > 0.5 else 'F'
                name = names.get_full_name(gender='male' if gender == 'M' else 'female')
                
                values.append([
                    name,
                    admission_date,
                    float(row['age']),
                    float(row['weight']),
                    gender,
                    float(row['platelets']),
                    float(row['spo2']),
                    float(row['creatinine']),
                    float(row['hematocrit']),
                    int(row['aids']),
                    int(row['lymphoma']),
                    int(row['solid_tumor_with_metastasis']),
                    float(row['heartrate']),
                    float(row['calcium']),
                    float(row['wbc']),
                    float(row['glucose']),
                    float(row['inr']),
                    float(row['potassium']),
                    float(row['sodium']),
                    int(row['ethnicity'])
                ])
            
            # Insert data into source database
            execute_values(source_cursor, """
                INSERT INTO patients (
                    name, admission_date, age, weight, gender,
                    platelets, spo2, creatinine, hematocrit,
                    aids, lymphoma, solid_tumor_with_metastasis,
                    heartrate, calcium, wbc, glucose,
                    inr, potassium, sodium, ethnicity
                ) VALUES %s
            """, values)
            
            # Commit source database changes
            source_conn.commit()
            
            # Clear web database
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM diabetes_predictor_alert;")
                cursor.execute("DELETE FROM diabetes_predictor_patient;")
            
            self.stdout.write(self.style.SUCCESS('Successfully initialized source database and cleared web database'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise
        finally:
            if 'source_cursor' in locals():
                source_cursor.close()
            if 'source_conn' in locals():
                source_conn.close()
