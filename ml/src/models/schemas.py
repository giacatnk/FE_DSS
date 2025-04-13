from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FeatureVector(BaseModel):
    age: float
    weight: float
    gender_M: int
    platelets: float
    spo2: float
    creatinine: float
    hematocrit: float
    aids: int
    lymphoma: int
    solid_tumor_with_metastasis: int
    heartrate: float
    calcium: float
    wbc: float
    glucose: float
    inr: float
    potassium: float
    sodium: float
    ethnicity: int

class PredictionRequest(BaseModel):
    patients: List[FeatureVector]

class PredictionResponse(BaseModel):
    predictions: List[dict]

class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: List[List[int]]

class TrainingStatus(BaseModel):
    status: str
    last_training_time: str | None
    error: str | None
    metrics: Optional[ModelMetrics]

class RetrainResponse(BaseModel):
    status: str
    message: str 