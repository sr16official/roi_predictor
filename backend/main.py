from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from roi_service import predict_rent, predict_price, calculate_roi


class Listing(BaseModel):
    size_sq_ft: float
    propertyType: str
    bedrooms: int
    latitude: float
    longitude: float
    localityName: str
    suburbName: str
    cityName: str
    companyName: str
    closest_metro_station_km: float
    AP_dist_km: float
    Aiims_dist_km: float
    NDRLW_dist_km: float


app = FastAPI(title="Rental ROI API", version="1.0.0")

# Allow local frontend (file:// or localhost) during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Rental ROI API is up"}


@app.post("/predict_rent")
async def api_predict_rent(listing: Listing):
    result = predict_rent(listing.dict())
    return {"predicted_rent": float(result)}


@app.post("/predict_price")
async def api_predict_price(listing: Listing):
    result = predict_price(listing.dict())
    return {"predicted_price": float(result)}


@app.post("/calculate_roi")
async def api_calculate_roi(listing: Listing):
    result = calculate_roi(listing.dict())
    # Ensure everything is JSON serializable (cast NumPy types to Python floats)
    return {
        "predicted_rent": float(result["predicted_rent"]),
        "predicted_price": float(result["predicted_price"]),
        "annual_rent": float(result["annual_rent"]),
        "gross_yield": float(result["gross_yield"]),
        "gross_yield_percent": float(result["gross_yield_percent"]),
    }
