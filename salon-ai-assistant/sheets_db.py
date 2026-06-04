import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_PATH = os.path.join(BASE_DIR, "credentials.json")
SHEET_NAME = "Salon Bookings"

BUSINESS_HOURS = [f"{hour:02d}:00" for hour in range(10, 19)]

# Authenticate and connect to Google Sheets
def get_sheet():
    if not os.path.exists(CREDS_PATH):
        raise FileNotFoundError(f"Missing {CREDS_PATH}. Please follow the setup guide to download it.")
        
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

def get_available_slots(branch: str, date: str) -> str:
    """Returns a comma-separated string of available slots for a given branch and date."""
    try:
        sheet = get_sheet()
    except Exception as e:
        return f"Error connecting to database: {str(e)}"
        
    records = sheet.get_all_records()
    
    booked_slots = {str(row.get('Time', '')) for row in records if str(row.get('Branch', '')) == branch and str(row.get('Date', '')) == date}
    
    available_slots = [slot for slot in BUSINESS_HOURS if slot not in booked_slots]
    
    if not available_slots:
        return "No slots available for this date."
    return ", ".join(available_slots)

def is_slot_available(branch: str, date: str, time: str) -> str:
    """Checks if a specific slot is available."""
    if time not in BUSINESS_HOURS:
        return f"Error: {time} is outside our business hours ({BUSINESS_HOURS[0]} - {BUSINESS_HOURS[-1]})."
        
    try:
        sheet = get_sheet()
    except Exception as e:
        return f"Error connecting to database: {str(e)}"
        
    records = sheet.get_all_records()
    
    for row in records:
        if str(row.get('Branch', '')) == branch and str(row.get('Date', '')) == date and str(row.get('Time', '')) == time:
            return f"Error: {time} is already booked."
            
    return "Available"

def book_slot(name: str, phone: str, branch: str, service: str, date: str, time: str) -> str:
    """Books a slot if available."""
    avail = is_slot_available(branch, date, time)
    if not avail == "Available":
        return avail
        
    try:
        sheet = get_sheet()
        # Row format: Name, Phone, Branch, Service, Date, Time
        new_row = [name, phone, branch, service, date, time]
        sheet.append_row(new_row)
        return f"Appointment confirmed for {name} on {date} at {time} for {service} at {branch}."
    except Exception as e:
        return f"Error: Could not save booking. Details: {str(e)}"
