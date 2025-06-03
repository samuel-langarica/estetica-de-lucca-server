from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import pytz
import os
import logging
from config import get_google_calendar_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

try:
    # Get credentials from environment variables
    credentials_info = get_google_calendar_config()
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES)
    
    # Create the service
    service = build('calendar', 'v3', credentials=credentials)
    logger.info("Successfully initialized Google Calendar service")
except Exception as e:
    logger.error(f"Failed to initialize Google Calendar service: {str(e)}")
    raise

calendar_id = 'samuel.langarica.m@gmail.com'

def get_events(start_date: datetime, end_date: datetime):
    """
    Get events from Google Calendar for the specified date range.
    
    Args:
        start_date: Start date for the query
        end_date: End date for the query
        
    Returns:
        List of simplified event dictionaries
    """
    try:
        # Ensure dates are timezone-aware
        if start_date.tzinfo is None:
            start_date = pytz.UTC.localize(start_date)
        if end_date.tzinfo is None:
            end_date = pytz.UTC.localize(end_date)
        
        # Convert datetime objects to RFC3339 format
        time_min = start_date.isoformat()
        time_max = end_date.isoformat()
        
        logger.info(f"Fetching events from {time_min} to {time_max}")
        
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
        
        logger.info(f"Successfully retrieved {len(simplified_events)} events")
        return simplified_events
        
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        raise

if __name__ == '__main__':
    print(get_events(datetime(2025, 6, 1), datetime(2025, 6, 30)))  