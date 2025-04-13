import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# File paths
TRAIN_DATA_PATH = DATA_DIR / "train_data.csv"
MODEL_PATH = MODELS_DIR / "model.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"

# Model parameters
MODEL_PARAMS = {
    "hidden_layer_sizes": (5, 3, 2),
    "activation": "relu",
    "solver": "adam",
    "max_iter": 1000,
    "random_state": 42
}

# Feature order for prediction
FEATURE_ORDER = [
    "age",
    "weight",
    "gender_M",
    "platelets",
    "spo2",
    "creatinine",
    "hematocrit",
    "aids",
    "lymphoma",
    "solid_tumor_with_metastasis",
    "heartrate",
    "calcium",
    "wbc",
    "glucose",
    "inr",
    "potassium",
    "sodium",
    "ethnicity"
] 