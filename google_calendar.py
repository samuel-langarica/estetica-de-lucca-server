from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import pytz
import os
from config import get_google_calendar_config

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Get credentials from environment variables
credentials_info = get_google_calendar_config()
credentials = service_account.Credentials.from_service_account_info(
    credentials_info, scopes=SCOPES)

# Create the service
service = build('calendar', 'v3', credentials=credentials)

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


if __name__ == '__main__':
    print(get_events(datetime(2025, 6, 1), datetime(2025, 6, 30)))  