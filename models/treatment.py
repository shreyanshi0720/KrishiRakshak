from pydantic import BaseModel

class TreatmentResponse(BaseModel):
    disease_name: str
    organic_treatments: str
    chemical_treatments: str
    preventive_measures: str

    class Config:
        from_attributes = True