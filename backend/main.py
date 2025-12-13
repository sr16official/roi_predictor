import os
import pathlib
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.roi_service import predict_rent, predict_price, calculate_roi


class Listing(BaseModel):
    size_sq_ft: float
    propertyType: str
    bedrooms: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    localityName: str
    suburbName: str
    cityName: str
    
    closest_metro_station_km: float
    
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


API_KEY = os.getenv("API_KEY")


def require_api_key(x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")) -> None:
    # For development/testing, make API key optional if not configured
    if not API_KEY:
        return  # Skip validation if API_KEY is not set
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    frontend_dir = pathlib.Path(__file__).resolve().parent.parent / "frontend"
    return FileResponse(str(frontend_dir / "index.html"))


@app.post("/predict_rent")
async def api_predict_rent(listing: Listing, _: None = Depends(require_api_key)):
    result = predict_rent(listing.dict())
    return {"predicted_rent": float(result)}


@app.post("/predict_price")
async def api_predict_price(listing: Listing, _: None = Depends(require_api_key)):
    result = predict_price(listing.dict())
    return {"predicted_price": float(result)}


@app.post("/calculate_roi")
async def api_calculate_roi(listing: Listing, _: None = Depends(require_api_key)):
    result = calculate_roi(listing.dict())
    # Ensure everything is JSON serializable (cast NumPy types to Python floats)
    return {
        "predicted_rent": float(result["predicted_rent"]),
        "predicted_price": float(result["predicted_price"]),
        "annual_rent": float(result["annual_rent"]),
        "gross_yield": float(result["gross_yield"]),
        "gross_yield_percent": float(result["gross_yield_percent"]),
    }


frontend_dir = pathlib.Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
