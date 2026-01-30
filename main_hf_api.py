from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging
import requests
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fish Disease Classifier API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aqua-health-pro.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API endpoint
HF_API_URL = "https://api-inference.huggingface.co/models/Saon110/fish-shrimp-disease-classifier"
HF_API_TOKEN = None  # Optional: Add your HF token for faster inference

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "online",
            "message": "Fish Disease Classifier API is running (using HF Inference API)",
            "model_loaded": True
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return JSONResponse(
        content={
            "status": "healthy",
            "model_loaded": True
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Predict fish disease from uploaded image using HF Inference API"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        logger.info(f"Processing image: {file.filename}")
        
        # Read uploaded file
        contents = await file.read()
        
        # Call Hugging Face Inference API
        headers = {}
        if HF_API_TOKEN:
            headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
        
        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=contents,
            timeout=30
        )
        
        if response.status_code == 503:
            raise HTTPException(
                status_code=503,
                detail="Model is loading on Hugging Face servers. Please try again in 20 seconds."
            )
        
        if response.status_code != 200:
            logger.error(f"HF API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=500,
                detail=f"Error from model API: {response.text}"
            )
        
        preds = response.json()
        logger.info(f"Predictions: {preds}")
        
        # Prepare results
        fish_preds = [
            pred for pred in preds
            if pred["label"].startswith("Fish_")
        ]
        
        if not fish_preds:
            top_prediction = preds[0] if preds else None
            if not top_prediction:
                raise HTTPException(
                    status_code=500,
                    detail="No predictions returned from model"
                )
            return JSONResponse(
                content={
                    "label": top_prediction["label"],
                    "score": float(top_prediction["score"])
                },
                headers={
                    "Access-Control-Allow-Origin": "*",
                }
            )
        
        top_fish = fish_preds[0]
        
        return JSONResponse(
            content={
                "label": top_fish["label"],
                "score": float(top_fish["score"])
            },
            headers={
                "Access-Control-Allow-Origin": "*",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
