# Diabetes Prediction API Specification

## Overview
This API provides endpoints for managing patient data, making predictions about diabetes risk, and managing the machine learning model. The system integrates with an external ML service running on localhost:8080 for prediction and training operations.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
No authentication is required for these endpoints.

## API Endpoints

### 1. Patients

#### GET /patients/
- **Description**: List all patients
- **Response**:
```json
{
    "count": integer,
    "next": string (URL),
    "previous": string (URL),
    "results": [
        {
            "id": integer,
            "name": string (nullable),
            "admission_date": string (datetime),
            "age": float,
            "weight": float,
            "gender": string (M/F/O),
            "platelets": float,
            "spo2": float,
            "creatinine": float,
            "hematocrit": float,
            "aids": integer,
            "lymphoma": integer,
            "solid_tumor_with_metastasis": integer,
            "heartrate": float,
            "calcium": float,
            "wbc": float,
            "glucose": float,
            "inr": float,
            "potassium": float,
            "sodium": float,
            "ethnicity": integer,
            "created_at": string (datetime),
            "updated_at": string (datetime)
        }
    ]
}
```

#### POST /patients/
- **Description**: Create a new patient and automatically trigger a prediction
- **Request**:
```json
{
    "name": string (nullable),
    "admission_date": string (datetime),
    "age": float,
    "weight": float,
    "gender": string (M/F/O),
    "platelets": float,
    "spo2": float,
    "creatinine": float,
    "hematocrit": float,
    "aids": integer,
    "lymphoma": integer,
    "solid_tumor_with_metastasis": integer,
    "heartrate": float,
    "calcium": float,
    "wbc": float,
    "glucose": float,
    "inr": float,
    "potassium": float,
    "sodium": float,
    "ethnicity": integer
}
```
- **Response**:
```json
{
    "id": integer,
    "name": string,
    "admission_date": string,
    "age": float,
    "weight": float,
    "gender": string,
    "platelets": float,
    "spo2": float,
    "creatinine": float,
    "hematocrit": float,
    "aids": integer,
    "lymphoma": integer,
    "solid_tumor_with_metastasis": integer,
    "heartrate": float,
    "calcium": float,
    "wbc": float,
    "glucose": float,
    "inr": float,
    "potassium": float,
    "sodium": float,
    "ethnicity": integer,
    "created_at": string,
    "updated_at": string,
    "prediction": {
        "id": integer,
        "prediction": boolean,
        "confidence": float,
        "model_version": string
    }
}
```

#### GET /patients/{id}/
- **Description**: Retrieve a specific patient
- **Response**: Same as GET /patients/ but single object

#### PUT /patients/{id}/
- **Description**: Update a patient's information
- **Request**: Same as POST /patients/ but partial updates allowed
- **Response**: Same as GET /patients/{id}/

#### DELETE /patients/{id}/
- **Description**: Delete a patient
- **Response**: 204 No Content

### 2. Alerts

#### GET /alerts/
- **Description**: List all alerts (predictions)
- **Response**:
```json
{
    "count": integer,
    "next": string (URL),
    "previous": string (URL),
    "results": [
        {
            "id": integer,
            "patient": integer,
            "patient_name": string,
            "prediction": boolean,
            "confidence": float,
            "model_version": string,
            "is_correct": boolean (nullable),
            "created_at": string
        }
    ]
}
```

#### GET /alerts/{id}/
- **Description**: Retrieve a specific alert
- **Response**: Same as GET /alerts/ but single object

#### POST /alerts/{id}/label/
- **Description**: Label an alert as correct or incorrect
- **Request**:
```json
{
    "is_correct": boolean
}
```
- **Response**:
```json
{
    "id": integer,
    "patient": integer,
    "patient_name": string,
    "prediction": boolean,
    "confidence": float,
    "model_version": string,
    "is_correct": boolean,
    "created_at": string
}
```

#### PUT /alerts/{id}/
- **Description**: Update alert details (including is_correct)
- **Request**:
```json
{
    "is_correct": boolean
}
```
- **Response**: Same as GET /alerts/{id}/

### 3. Models

#### POST /models/retrain/
- **Description**: Retrain the model with latest labeled data
- **Request**: None
- **Response**:
```json
{
    "status": "success",
    "version": string,
    "accuracy": float
}
```

#### GET /models/status/
- **Description**: Get current model status
- **Response**:
```json
{
    "version": string,
    "accuracy": float,
    "created_at": string
}
```

## Data Flow

1. **Prediction Flow**
   - When a new patient is created, their data is automatically sent to the ML service at `/predict`
   - The ML service returns a prediction and confidence score
   - The prediction is stored in the database with the model version used
   - The prediction result is returned to the frontend

2. **Retraining Flow**
   - When `/models/retrain/` is called:
     1. The system collects all labeled alerts from the database
     2. The data is sent to the ML service at `/retrain`
     3. The ML service returns a new model version and accuracy
     4. The new model metadata is stored in the database
     5. The previous model is marked as inactive

3. **Labeling Flow**
   - When an alert is labeled as correct/incorrect:
     1. The label is stored in the database
     2. The data becomes available for future retraining

## Error Responses
All endpoints may return the following error responses:

```json
{
    "error": string
}
```

## Notes
1. All dates are in ISO format (YYYY-MM-DDTHH:MM:SS)
2. Model versions are timestamp-based (YYYYMMDD_HHMMSS)
3. Confidence scores are between 0 and 1
4. The ML service runs on localhost:8080
5. All endpoints are rate-limited to prevent abuse
6. The system maintains a history of all predictions and model versions
