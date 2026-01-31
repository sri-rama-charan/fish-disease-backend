from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging
import traceback
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fish Disease Classifier API")

# CORS Configuration - Allow your frontend
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

# HuggingFace configuration
HF_API_URL = "https://api-inference.huggingface.co/models/Saon110/fish-shrimp-disease-classifier"
HF_TOKEN = os.getenv('HF_TOKEN')

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "online",
            "message": "Fish Disease Classifier API is running",
            "model_loaded": True,
            "using": "HuggingFace Inference API"
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
            "model_loaded": True,
            "using": "HuggingFace Inference API"
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Predict fish disease from uploaded image using HuggingFace Inference API"""
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
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert image to bytes for API
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Call HuggingFace Inference API
        headers = {}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"
        
        logger.info("Calling HuggingFace Inference API...")
        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=img_byte_arr,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"HuggingFace API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=503,
                detail=f"Model inference failed: {response.text}"
            )
        
        preds = response.json()
        logger.info(f"Predictions: {preds}")
        
        # Prepare results
        fish_preds = [
            pred for pred in preds
            if pred["label"].startswith("Fish_")
        ]
        
        if not fish_preds:
            # If no fish predictions, return top prediction anyway
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
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
