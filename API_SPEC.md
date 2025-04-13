# API Specification

## Base URL
```
http://localhost:8000/api/
```

## Authentication
- No authentication required for any endpoints
- All endpoints are public

## Endpoints

### 1. Patients

#### 1.1 List Patients
```
GET /patients/
```
- Returns a list of all patients
- Response:
```json
{
    "count": integer,
    "next": string (URL),
    "previous": string (URL),
    "results": [
        {
            "id": integer,
            "name": string,
            "admission_date": string (date),
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
            "latest_alert": {
                "id": integer,
                "prediction": boolean,
                "confidence": float,
                "model_version": string,
                "created_at": string (datetime)
            }
        }
    ]
}
```

#### 1.2 Create Patient
```
POST /patients/
```
- Request Body:
```json
{
    "name": string,
    "admission_date": string (date),
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
    "ethnicity": integer
}
```
- Response:
```json
{
    "id": integer,
    "name": string,
    "admission_date": string (date),
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
    "latest_alert": {
        "id": integer,
        "prediction": boolean,
        "confidence": float,
        "model_version": string,
        "created_at": string (datetime)
    }
}
```

#### 1.3 Sync Patients
```
GET /patients/sync/
```
- Description: Syncs up to 10 patients from source database to web database
- Response:
```json
{
    "patients": [
        {
            "id": integer,
            "name": string,
            "admission_date": string (date),
            "latest_alert": {
                "id": integer,
                "prediction": boolean,
                "confidence": float,
                "model_version": string,
                "created_at": string (datetime)
            }
        }
    ],
    "total_synced": integer
}
```

### 2. Alerts

#### 2.1 List Alerts
```
GET /alerts/
```
- Returns a list of all alerts
- Response:
```json
{
    "count": integer,
    "next": string (URL),
    "previous": string (URL),
    "results": [
        {
            "id": integer,
            "patient": {
                "id": integer,
                "name": string
            },
            "prediction": boolean,
            "confidence": float,
            "model_version": string,
            "created_at": string (datetime),
            "is_correct": boolean
        }
    ]
}
```

#### 2.2 Mark Alert as False Prediction
```
POST /alerts/{alert_id}/mark_false_prediction/
```
- Description: Marks an alert as having a false prediction
- Response:
```json
{
    "message": "Alert marked as false prediction"
}
```

### 3. Models

#### 3.1 Get Model Status
```
GET /models/
```
- Returns the current model status
- Response:
```json
{
    "version": string,
    "status": string,
    "last_trained": string (datetime)
}
```

#### 3.2 Train Model
```
POST /models/train/
```
- Description: Starts the model training process
- Response:
```json
{
    "message": "Model training started"
}
```

### 4. Predictions

#### 4.1 Get Predictions
```
POST /patients/predict/
```
- Request Body:
```json
[
    {
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
        "ethnicity": integer
    }
]
```
- Response:
```json
{
    "predictions": [
        {
            "prediction": float,
            "confidence": float
        }
    ],
    "model_version": string,
    "status": string
}
```

## Error Responses
All endpoints may return error responses with the following format:
```json
{
    "error": string
}
```

## Status Codes
- 200: Success
- 201: Created (for POST requests)
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error
