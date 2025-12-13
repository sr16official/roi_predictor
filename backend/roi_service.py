import pathlib
from typing import Dict, Any
import logging

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base path for model artifacts
BASE_DIR = pathlib.Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# Global variables for models and features
rent_model = None
rent_feature_columns = None
house_model = None
house_feature_columns = None
models_loaded = False


def load_models():
    """Load models and feature columns with error handling"""
    global rent_model, rent_feature_columns, house_model, house_feature_columns, models_loaded
    
    if models_loaded:
        return True
    
    try:
        # Load rent model
        rent_model_path = MODELS_DIR / "rent_price_model.json"
        rent_features_path = MODELS_DIR / "rent_feature_columns.joblib"
        
        if rent_model_path.exists() and rent_features_path.exists():
            rent_model = xgb.Booster()
            rent_model.load_model(str(rent_model_path))
            rent_feature_columns = joblib.load(str(rent_features_path))
            logger.info("Rent model loaded successfully")
        else:
            logger.warning("Rent model files not found")
        
        # Load housing model
        house_model_path = MODELS_DIR / "housing_xgb_model.json"
        house_features_path = MODELS_DIR / "Housing_feature.joblib"
        
        if house_model_path.exists() and house_features_path.exists():
            house_model = xgb.Booster()
            house_model.load_model(str(house_model_path))
            house_feature_columns = joblib.load(str(house_features_path))
            logger.info("Housing model loaded successfully")
        else:
            logger.warning("Housing model files not found")
        
        models_loaded = True
        return True
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        models_loaded = True  # Mark as attempted to avoid repeated failures
        return False


# Try to load models on import
try:
    load_models()
except Exception as e:
    logger.error(f"Failed to load models on import: {e}")
    models_loaded = True  # Mark as attempted to avoid repeated failures


def preprocess_for_model(sample_dict: Dict[str, Any], feature_columns) -> xgb.DMatrix:
    """Prepare a single sample for prediction.

    - Convert dict to one-row DataFrame
    - Apply get_dummies(drop_first=True)
    - Reindex to model feature columns, filling missing with 0
    - Return xgboost.DMatrix
    """

    # Map API field names to model field names for housing model
    processed_dict = sample_dict.copy()
    if 'size_sq_ft' in processed_dict and 'area' not in processed_dict:
        processed_dict['area'] = processed_dict['size_sq_ft']
    
    df = pd.DataFrame([processed_dict])
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Align with training-time feature columns
    df_aligned = df_encoded.reindex(columns=feature_columns, fill_value=0)

    dmatrix = xgb.DMatrix(df_aligned)
    return dmatrix


def predict_rent(sample_dict: Dict[str, Any]) -> float:
    """Predict rent price with fallback for missing models"""
    if rent_model is None or rent_feature_columns is None:
        # Fallback calculation based on size and location
        size_sq_ft = sample_dict.get('size_sq_ft', 1000)
        bedrooms = sample_dict.get('bedrooms', 2)
        
        # Simple fallback formula: base rate + size premium + bedroom premium
        base_rent = 8000
        size_rate = 15  # per sq ft
        bedroom_premium = 2000 * bedrooms
        
        predicted_rent = base_rent + (size_sq_ft * size_rate) + bedroom_premium
        logger.warning(f"Using fallback rent prediction: {predicted_rent}")
        return float(predicted_rent)
    
    try:
        dmatrix = preprocess_for_model(sample_dict, rent_feature_columns)
        pred = rent_model.predict(dmatrix)
        return float(pred[0])
    except Exception as e:
        logger.error(f"Rent prediction failed: {e}")
        # Fallback to simple calculation
        size_sq_ft = sample_dict.get('size_sq_ft', 1000)
        return float(8000 + size_sq_ft * 15)


def predict_price(sample_dict: Dict[str, Any]) -> float:
    """Predict housing price with fallback for missing models"""
    if house_model is None or house_feature_columns is None:
        # Fallback calculation based on size and bedrooms
        size_sq_ft = sample_dict.get('size_sq_ft', 1200)
        bedrooms = sample_dict.get('bedrooms', 2)
        
        # Simple fallback formula: base price + size rate + bedroom premium
        base_price = 5000000  # 50 lakh base
        size_rate = 8000  # per sq ft
        bedroom_premium = 500000 * bedrooms  # 5 lakh per bedroom
        
        predicted_price = base_price + (size_sq_ft * size_rate) + bedroom_premium
        logger.warning(f"Using fallback price prediction: {predicted_price}")
        return float(predicted_price)
    
    try:
        dmatrix = preprocess_for_model(sample_dict, house_feature_columns)
        pred = house_model.predict(dmatrix)
        return float(pred[0])
    except Exception as e:
        logger.error(f"Price prediction failed: {e}")
        # Fallback to simple calculation
        size_sq_ft = sample_dict.get('size_sq_ft', 1200)
        return float(5000000 + size_sq_ft * 8000)


def calculate_roi(sample_dict: Dict[str, Any]) -> Dict[str, float]:
    predicted_rent = predict_rent(sample_dict)
    predicted_price = predict_price(sample_dict)

    annual_rent = predicted_rent * 12.0

    if predicted_price is None or predicted_price == 0:
        gross_yield = 0.0
    else:
        gross_yield = annual_rent / predicted_price

    gross_yield_percent = gross_yield * 100.0

    return {
        "predicted_rent": float(predicted_rent),
        "predicted_price": float(predicted_price),
        "annual_rent": float(annual_rent),
        "gross_yield": float(gross_yield),
        "gross_yield_percent": float(gross_yield_percent),
    }
