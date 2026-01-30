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

print("Loading model...")

# Load your model using Hugging Face pipeline
classifier = pipeline(
    "image-classification",
    model="Saon110/fish-shrimp-disease-classifier",
)

print("Model loaded")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # Read uploaded file
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Run the model
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
