from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config.database import init_db
from routes import auth, detection, treatment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="KrishiRakshak API",
    description="AI-powered crop disease detection and management system",
    version="1.0.0"
)

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(detection.router, prefix="/detection", tags=["Disease Detection"])
app.include_router(treatment.router, prefix="/treatment", tags=["Treatments"])

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to KrishiRakshak API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}