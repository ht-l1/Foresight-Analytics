from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.config.settings import AppConfig
from app.utils.logger import get_logger
from app.data.data_loader import DataLoader
from app.models.forecaster import Forecaster
import pandas as pd
from fastapi.responses import JSONResponse
from typing import List
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

logger = get_logger(__name__)

# Initilization
app = FastAPI(
    title=AppConfig.APP_NAME,
    version=AppConfig.VERSION,
    debug=AppConfig.DEBUG
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  
)
logger.info("CORS middleware initialized")

class ForecastRequest(BaseModel):
    months: int
    region: Optional[str] = None
    category: Optional[str] = None

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error at {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": f"Internal server error: {str(exc)}"}
    )

# Endpoints below
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Foresight Analytics API"}

@app.post("/forecast")
async def forecast(request: ForecastRequest):
    try:
        # Validate months
        if request.months < 1 or request.months > 48:
            raise HTTPException(status_code=400, detail="Months must be between 1 and 48")

        # Initialize data loader
        data_loader = DataLoader()
        
        # Load data
        if not data_loader.check_data_exists():
            raise HTTPException(status_code=503, detail="No data available in database")
        
        df = data_loader.get_all_data()
        if df.empty:
            raise HTTPException(status_code=503, detail="Failed to load data")

        # Apply filters
        filtered_df = df.copy()
        if request.region and request.region != "All":
            if request.region not in data_loader.get_regions():
                raise HTTPException(status_code=400, detail=f"Invalid region: {request.region}")
            filtered_df = filtered_df[filtered_df['region'] == request.region]
        if request.category and request.category != "All":
            if request.category not in data_loader.get_categories():
                raise HTTPException(status_code=400, detail=f"Invalid category: {request.category}")
            filtered_df = filtered_df[filtered_df['category'] == request.category]

        if filtered_df.empty:
            raise HTTPException(status_code=400, detail="No data matches the selected filters")

        # Generate forecasts
        forecaster = Forecaster()
        forecast_results = forecaster.forecast(filtered_df, request.months)

        # Format response
        response = {
            "status": "success",
            "data": {
                "forecasts": {},
                "metrics": {}
            }
        }

        for model_name, result in forecast_results.items():
            if not result['forecast'].empty:
                # Convert DataFrame to list of dicts for JSON serialization
                response['data']['forecasts'][model_name] = result['forecast'].to_dict(orient='records')
                response['data']['metrics'][model_name] = result['metrics']

        logger.info(f"Forecast generated for {request.months} months")
        return response

    except Exception as e:
        logger.error(f"Forecast error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecast generation failed: {str(e)}")
    
class FilterRequest(BaseModel):
    region: Optional[str] = None
    category: Optional[str] = None
    limit: Optional[int] = 1000
    offset: Optional[int] = 0

@lru_cache(maxsize=32)
def cached_get_all_data() -> pd.DataFrame:
    data_loader = DataLoader()
    return data_loader.get_all_data()

@app.get("/data", response_model=dict)
async def get_data():
    try:
        df = cached_get_all_data()
        if df.empty:
            raise HTTPException(status_code=503, detail="No data available")
        
        # Convert order_date to ISO format string for JSON serialization
        df = df.copy()
        if 'order_date' in df.columns:
            df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        data_loader = DataLoader()
        response = {
            "status": "success",
            "data": df.to_dict(orient='records'),
            "metadata": {
                "total_records": len(df),
                "regions": data_loader.get_regions(),
                "categories": data_loader.get_categories(),
                "segments": data_loader.get_segments()
            }
        }
        logger.info("Retrieved all data")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Data retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")

@app.post("/data/filter", response_model=dict)
async def filter_data(request: FilterRequest):
    try:
        data_loader = DataLoader()
        
        # Validate inputs
        if request.region and request.region != "All" and request.region not in data_loader.get_regions():
            raise HTTPException(status_code=400, detail=f"Invalid region: {request.region}")
        if request.category and request.category != "All" and request.category not in data_loader.get_categories():
            raise HTTPException(status_code=400, detail=f"Invalid category: {request.category}")
        if request.limit < 1 or request.limit > 10000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 10000")
        if request.offset < 0:
            raise HTTPException(status_code=400, detail="Offset cannot be negative")

        # Load and filter data
        df = cached_get_all_data()
        filtered_df = df.copy()
        
        if request.region and request.region != "All":
            filtered_df = filtered_df[filtered_df['region'] == request.region]
        if request.category and request.category != "All":
            filtered_df = filtered_df[filtered_df['category'] == request.category]

        if filtered_df.empty:
            raise HTTPException(status_code=400, detail="No data matches the selected filters")

        # Convert order_date to ISO format string for JSON serialization
        if 'order_date' in filtered_df.columns:
            filtered_df['order_date'] = filtered_df['order_date'].dt.strftime('%Y-%m-%dT%H:%M:%S')

        # Apply pagination
        total_records = len(filtered_df)
        filtered_df = filtered_df.iloc[request.offset:request.offset + request.limit]

        response = {
            "status": "success",
            "data": filtered_df.to_dict(orient='records'),
            "metadata": {
                "total_records": total_records,
                "returned_records": len(filtered_df),
                "offset": request.offset,
                "limit": request.limit
            }
        }
        logger.info(f"Filtered data: {len(filtered_df)} records returned")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Data filter error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data filter failed: {str(e)}")
    
@app.get("/health", response_model=dict)
async def health_check():
    try:
        data_loader = DataLoader()
        db_status = data_loader.check_data_exists()
        return {
            "status": "healthy",
            "database": "connected" if db_status else "empty",
            "version": AppConfig.VERSION
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")