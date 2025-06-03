from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import pytz
import os
import json

# Carga las credenciales
SERVICE_ACCOUNT_FILE = 'calendar-access.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Try to get credentials from environment variable first, fall back to file if not found
if 'GOOGLE_CALENDAR_JSON' in os.environ:
    credentials_info = json.loads(os.environ['GOOGLE_CALENDAR_JSON'])
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES)
else:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Crear el servicio
service = build('calendar', 'v3', credentials=credentials)

# ID del calendario (usualmente email del usuario que compartió su calendario)
calendar_id = 'samuel.langarica.m@gmail.com'

def get_events(start_date: datetime, end_date: datetime):
    # Ensure dates are timezone-aware
    if start_date.tzinfo is None:
        start_date = pytz.UTC.localize(start_date)
    if end_date.tzinfo is None:
        end_date = pytz.UTC.localize(end_date)
    
    # Convert datetime objects to RFC3339 format
    time_min = start_date.isoformat()
    time_max = end_date.isoformat()
    
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=1000,
        timeMin=time_min,
        timeMax=time_max
    ).execute()
    
    events = events_result.get('items', [])
    simplified_events = []
    
    for event in events:
        simplified_events.append({
            'name': event.get('summary', 'No Title'),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date'))
        })
    
    return simplified_events


print(get_events(datetime(2025, 6, 1), datetime(2025, 6, 30)))  