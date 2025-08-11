# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # or ["http://localhost:3000"] for security
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/api/health")
def health():
  try:
    return "Hi, the API is running!"
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
