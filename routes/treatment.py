from fastapi import APIRouter, HTTPException, Depends
import sqlite3

from models.treatment import TreatmentResponse
from utils.database import get_db

router = APIRouter()

@router.get("/{disease_name}", response_model=TreatmentResponse)
async def get_treatment(disease_name: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM treatments WHERE disease_name = ?", (disease_name,))
    treatment = cursor.fetchone()
    
    if treatment:
        return {
            "disease_name": treatment[1],
            "organic_treatments": treatment[2],
            "chemical_treatments": treatment[3],
            "preventive_measures": treatment[4]
        }
    else:
        raise HTTPException(status_code=404, detail="Treatment not found")

@router.get("/")
async def get_all_treatments(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    
    return [
        {
            "disease_name": t[1],
            "organic_treatments": t[2],
            "chemical_treatments": t[3],
            "preventive_measures": t[4]
        }
        for t in treatments
    ]