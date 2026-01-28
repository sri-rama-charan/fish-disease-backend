from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
import io

app = FastAPI()

# Allow Flutter app to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

# Global variable to store the model
model_pipeline = None

def get_model():
    global model_pipeline
    if model_pipeline is None:
        print("Loading model...")
        model_pipeline = pipeline(
            "image-classification",
            model="Saon110/fish-shrimp-disease-classifier",
            token=os.environ.get("HF_TOKEN")
        )
        print("Model loaded")
    return model_pipeline

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # Read uploaded file
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Run the model
    classifier = get_model()
    preds = classifier(image)

    # Prepare results
    fish_preds = [
        pred for pred in preds
        if pred["label"].startswith("Fish_")
    ]

    top_fish = fish_preds[0]

    return {
        "label": top_fish["label"],
        "score": float(top_fish["score"])
    }

