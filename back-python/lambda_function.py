from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import Optional
import uvicorn
import numpy as np
from analyse import analyze_ecg, save_dataset, get_ecg_plot_base64_from_color_choice, get_random_dataset_by_color, get_random_color
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Score

UPLOAD_FOLDER = '/tmp'
app = FastAPI()
Base.metadata.create_all(bind=engine)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def to_python_type(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: to_python_type(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_python_type(v) for v in obj]
    else:
        return obj

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/analyze")
async def analyze(
    file: Optional[UploadFile] = File(None),
    color_choice: str = Form("green"),
    model_choice: str = Form("cnn")
):
    saved_path = None

    # If a file is given, save it to the upload folder 
    if file is not None:
        saved_path = save_dataset(file, UPLOAD_FOLDER)
    else:
        saved_path = get_random_dataset_by_color(color_choice)

    # Skicka in allt som argument, inget med globals längre
    try:
        result = analyze_ecg(file_path=saved_path, model_choice=model_choice)
        return to_python_type(result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get-random-plot")
async def get_random_plot():
    try:
        # Get a random color choice from the available datasets
        color_choice = get_random_color()
        # Get a random ECG plot in base64 format
        result = get_ecg_plot_base64_from_color_choice(color_choice)
        return to_python_type(result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/score")
def create_score(value: int, db: Session = Depends(get_db)):
    score = Score(value=value)
    db.add(score)
    db.commit()
    db.refresh(score)
    return JSONResponse(content="Score saved", status_code=201)

@app.get("/score/stats")
def get_average_score(db: Session = Depends(get_db)):
    scores = db.query(Score).all()
    if not scores:
        return {"average": 0, "numberOfUsers": 0}
    average = sum(score.value for score in scores) / len(scores)
    return JSONResponse(content={"average": average, "numberOfUsers": len(scores)}, status_code=200)

@app.get("/")
def index():
    return "Welcome to the ECG Prediction API! Use the endpoints to analyze ECG data, get random plots, and submit scores."

# Lambda handler
handler = Mangum(app)

# For local development
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


