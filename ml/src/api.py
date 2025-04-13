from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from src.trainer import ModelTrainer
from src.scheduler import TrainingScheduler
from src.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    TrainingStatus,
    RetrainResponse
)
from src.config import TRAIN_DATA_PATH, MODEL_PATH, SCALER_PATH, MODEL_PARAMS, FEATURE_ORDER
import threading
import time
import os

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # This will override any existing handlers
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="ML Model API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize components
trainer = ModelTrainer()
scheduler = TrainingScheduler(trainer)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting ML API server...")
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=scheduler.start)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logger.info("Training scheduler started")
    
    logger.info(f"ML API server is running on port 8000")
    logger.info(f"Training data path: {TRAIN_DATA_PATH}")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Scaler path: {SCALER_PATH}")

@app.get("/")
async def root():
    return {"message": "ML Model API is running"}

@app.get("/status", response_model=TrainingStatus)
async def get_status():
    """Get the current status of the training process."""
    try:
        return trainer.get_status()
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make predictions using the trained model."""
    try:
        predictions = []
        for patient in request.patients:
            # Convert patient dict to list of features in the correct order
            features = [getattr(patient, feature) for feature in FEATURE_ORDER]
            prediction = trainer.predict(features)
            predictions.append({
                "prediction": float(prediction)
            })
        
        return {"predictions": predictions}
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain", response_model=RetrainResponse)
async def trigger_retraining():
    """Trigger immediate model retraining."""
    try:
        return scheduler.trigger_retraining()
    except Exception as e:
        logger.error(f"Error triggering retraining: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 