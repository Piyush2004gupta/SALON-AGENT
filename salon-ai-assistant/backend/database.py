import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bookings.db")

# Default salon hours (10 AM to 6 PM)
BUSINESS_HOURS = [f"{hour:02d}:00" for hour in range(10, 19)]

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                branch TEXT NOT NULL,
                service TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                UNIQUE(branch, date, time)
            )
        ''')
        conn.commit()

def get_available_slots(branch: str, date: str) -> str:
    """Returns a comma-separated string of available slots for a given branch and date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT time FROM bookings 
            WHERE branch = ? AND date = ?
        ''', (branch, date))
        booked_slots = {row[0] for row in cursor.fetchall()}
        
        available_slots = [slot for slot in BUSINESS_HOURS if slot not in booked_slots]
        
        if not available_slots:
            return "No slots available for this date."
        return ", ".join(available_slots)

def is_slot_available(branch: str, date: str, time: str) -> str:
    """Checks if a specific slot is available."""
    if time not in BUSINESS_HOURS:
        return f"Error: {time} is outside our business hours ({BUSINESS_HOURS[0]} - {BUSINESS_HOURS[-1]})."
        
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM bookings 
            WHERE branch = ? AND date = ? AND time = ?
        ''', (branch, date, time))
        result = cursor.fetchone()
        
        if result:
            return f"Error: {time} is already booked."
        return "Available"

def book_slot(name: str, phone: str, branch: str, service: str, date: str, time: str) -> str:
    """Books a slot if available."""
    avail = is_slot_available(branch, date, time)
    if not avail == "Available":
        return avail
        
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bookings (name, phone, branch, service, date, time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, phone, branch, service, date, time))
            conn.commit()
            return f"Appointment confirmed for {name} on {date} at {time} for {service} at {branch}."
    except sqlite3.IntegrityError:
        return f"Error: {time} was just booked by someone else."

# Initialize DB on import
init_db()
