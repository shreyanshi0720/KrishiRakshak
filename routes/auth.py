from fastapi import APIRouter, HTTPException, Depends
import sqlite3

from models.user import UserCreate, UserResponse, UserLogin
from utils.database import get_db
from utils.security import hash_password, verify_password

router = APIRouter()

@router.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", 
                  (user.username, user.email))
    existing_user = cursor.fetchone()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = hash_password(user.password)
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)",
            (user.username, user.email, hashed_password, user.full_name)
        )
        db.commit()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,))
        new_user = cursor.fetchone()
        
        return {
            "id": new_user[0],
            "username": new_user[1],
            "email": new_user[2],
            "full_name": new_user[4],
            "created_at": new_user[5]
        }
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database error")

@router.post("/login/")
async def login_user(credentials: UserLogin, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (credentials.username,))
    user = cursor.fetchone()
    
    if user and verify_password(credentials.password, user[3]):
        return {"message": "Login successful", "user_id": user[0]}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")