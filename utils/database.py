import sqlite3

def get_db():
    conn = sqlite3.connect('krishirakshak.db')
    try:
        yield conn
    finally:
        conn.close()