import pathlib
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb

# Base path for model artifacts
BASE_DIR = pathlib.Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"


# Load models and feature columns
rent_model_path = MODELS_DIR / "rent_price_model.json"
rent_features_path = MODELS_DIR / "rent_feature_columns.joblib"
house_model_path = MODELS_DIR / "housing_xgb_model.json"
house_features_path = MODELS_DIR / "Housing_feature.joblib"


rent_model = xgb.Booster()
rent_model.load_model(str(rent_model_path))

rent_feature_columns = joblib.load(str(rent_features_path))

house_model = xgb.Booster()
house_model.load_model(str(house_model_path))

house_feature_columns = joblib.load(str(house_features_path))


def preprocess_for_model(sample_dict: Dict[str, Any], feature_columns) -> xgb.DMatrix:
    """Prepare a single sample for prediction.

    - Convert dict to one-row DataFrame
    - Apply get_dummies(drop_first=True)
    - Reindex to model feature columns, filling missing with 0
    - Return xgboost.DMatrix
    """

    df = pd.DataFrame([sample_dict])
    df_encoded = pd.get_dummies(df, drop_first=True)

    # Align with training-time feature columns
    df_aligned = df_encoded.reindex(columns=feature_columns, fill_value=0)

    dmatrix = xgb.DMatrix(df_aligned)
    return dmatrix


def predict_rent(sample_dict: Dict[str, Any]) -> float:
    dmatrix = preprocess_for_model(sample_dict, rent_feature_columns)
    pred = rent_model.predict(dmatrix)
    # Booster.predict returns an array; take the first element
    return float(pred[0])


def predict_price(sample_dict: Dict[str, Any]) -> float:
    dmatrix = preprocess_for_model(sample_dict, house_feature_columns)
    pred = house_model.predict(dmatrix)
    return float(pred[0])


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
