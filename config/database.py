import sqlite3
import os


def init_db():
    """
    Initialize the application database with required tables and initial data.
    
    Creates three main tables:
    1. users - For storing user account information
    2. detections - For storing plant disease detection history
    3. treatments - For storing disease treatment recommendations
    
    Also pre-populates the treatments table with common plant disease treatments.
    """
    conn = sqlite3.connect('krishirakshak.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_path TEXT NOT NULL,
        plant_type TEXT,
        disease_name TEXT,
        confidence REAL,
        treatment_advice TEXT,
        detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_name TEXT UNIQUE NOT NULL,
        organic_treatments TEXT,
        chemical_treatments TEXT,
        preventive_measures TEXT
    )
    ''')

    treatments_data = [
        ('Apple Scab', 
         'Apply sulfur or lime sulfur sprays', 
         'Use fungicides containing myclobutanil or trifloxystrobin', 
         'Remove infected leaves and practice good sanitation'),
        
        ('Powdery Mildew', 
         'Apply milk spray or baking soda solution', 
         'Use fungicides containing myclobutanil or propiconazole', 
         'Ensure good air circulation and avoid overhead watering'),
        
        ('Early Blight', 
         'Apply copper-based fungicides', 
         'Use chlorothalonil or mancozeb', 
         'Rotate crops and remove infected plant debris'),
        
        ('Late Blight', 
         'Remove and destroy infected plants', 
         'Apply fungicides containing chlorothalonil or copper', 
         'Avoid overhead watering and space plants properly'),
        
        ('Leaf Spot', 
         'Apply neem oil or baking soda solution', 
         'Use fungicides containing chlorothalonil or thiophanate-methyl', 
         'Water at the base of plants and improve air circulation'),
        
        ('Healthy', 
         'No treatment needed', 
         'No chemical treatment needed', 
         'Maintain good plant health practices')
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO treatments 
    (disease_name, organic_treatments, chemical_treatments, preventive_measures)
    VALUES (?, ?, ?, ?)
    ''', treatments_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully")


if __name__ == "__main__":
    init_db()