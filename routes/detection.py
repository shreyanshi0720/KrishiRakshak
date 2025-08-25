from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
import sqlite3
import os
import uuid
from datetime import datetime

from ml.model import DiseaseDetectionModel
from models.detection import DetectionResponse
from utils.database import get_db

router = APIRouter()
ml_model = DiseaseDetectionModel()

def get_treatment_advice(disease_name: str, db: sqlite3.Connection) -> str:
    cursor = db.cursor()
    cursor.execute("SELECT * FROM treatments WHERE disease_name = ?", (disease_name,))
    treatment = cursor.fetchone()
    
    if treatment:
        return f"Organic: {treatment[1]}. Chemical: {treatment[2]}. Prevention: {treatment[3]}"
    else:
        return "General advice: Consult with agricultural expert for specific treatment recommendations."

@router.post("/detect-disease/")
async def detect_disease(
    image: UploadFile = File(...),
    plant_type: str = Form(...),
    user_id: int = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    """Detect disease from plant image"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    try:
        contents = await image.read()

        disease_name, confidence = ml_model.predict(contents)
        
        treatment_advice = get_treatment_advice(disease_name, db)
  
        os.makedirs("uploads", exist_ok=True)
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join("uploads", filename)
        
        with open(filepath, "wb") as f:
            f.write(contents)

        cursor.execute(
            "INSERT INTO detections (user_id, image_path, plant_type, disease_name, confidence, treatment_advice) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, filepath, plant_type, disease_name, confidence, treatment_advice)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM detections WHERE id = ?", (cursor.lastrowid,))
        detection = cursor.fetchone()
        
        return {
            "detection_id": detection[0],
            "plant_type": plant_type,
            "disease_name": disease_name,
            "confidence": confidence,
            "treatment_advice": treatment_advice,
            "detected_at": detection[7]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.get("/history/{user_id}", response_model=list[DetectionResponse])
async def get_detection_history(user_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Get detection history for a user"""
    cursor = db.cursor()
    cursor.execute("SELECT * FROM detections WHERE user_id = ? ORDER BY detected_at DESC", (user_id,))
    detections = cursor.fetchall()
    
    return [
        {
            "id": d[0],
            "user_id": d[1],
            "plant_type": d[3],
            "disease_name": d[4],
            "confidence": d[5],
            "treatment_advice": d[6],
            "detected_at": d[7]
        }
        for d in detections
    ]