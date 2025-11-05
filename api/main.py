from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import json
from datetime import datetime
import os

app = FastAPI()

# Load trained model
model = joblib.load("sentiment_model.pkl")

# logs directory 
os.makedirs("logs", exist_ok=True)
LOG_DIR = "logs" 
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "prediction_logs.json")


class PredictionRequest(BaseModel):
    text: str
    true_sentiment: str = None  # Optional feedback

@app.post("/predict")
def predict(req: PredictionRequest):
    try:
        # Simple prediction using the model
        pred = model.predict([req.text])[0]

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "request_text": req.text,
            "predicted_sentiment": pred,
            "true_sentiment": req.true_sentiment
        }

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {"predicted_sentiment": pred}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
