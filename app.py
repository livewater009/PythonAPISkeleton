# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
from palm_detect import PalmDetector  # assuming your class is named like this
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
detector = PalmDetector()  # or however you instantiate it

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # or ["http://localhost:3000"] for security
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class ImageRequest(BaseModel):
  image: str

@app.post("/api/detect-palm")
def analyze_palm(data: ImageRequest) -> Dict[str, Any]:
  try:
    result = detector.detect_palm_features(data.image)
    return result
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
