from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import pipeline
from PIL import Image
import io
import logging
import traceback

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

# Global variable for model
classifier = None

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global classifier
    try:
        logger.info("Loading model with memory optimization...")
        import torch
        # Use torch hub cache cleanup
        torch.hub.set_dir('/tmp/torch_cache')
        
        classifier = pipeline(
            "image-classification",
            model="Saon110/fish-shrimp-disease-classifier",
            device=-1,  # Force CPU
            model_kwargs={
                "low_cpu_mem_usage": True,  # Reduce memory during loading
                "torch_dtype": torch.float16  # Use half precision
            }
        )
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.error(traceback.format_exc())

@app.get("/")
async def root():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "online",
            "message": "Fish Disease Classifier API is running",
            "model_loaded": classifier is not None
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
            "status": "healthy" if classifier else "model_not_loaded",
            "model_loaded": classifier is not None
        },
        headers={
            "Access-Control-Allow-Origin": "*",
        }
    )

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Predict fish disease from uploaded image"""
    try:
        # Check if model is loaded
        if classifier is None:
            raise HTTPException(
                status_code=503,
                detail="Model not loaded yet. Please wait and try again."
            )
        
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
        
        # Run the model
        logger.info("Running prediction...")
        preds = classifier(image)
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
