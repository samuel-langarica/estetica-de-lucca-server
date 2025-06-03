from datetime import datetime, timedelta
from typing import Dict, List
from google_calendar import get_events
import pytz

# Schedule configuration (in Mexico City time)
SCHEDULE = {
    'weekday': {
        'start': '10:00',
        'end': '19:00'
    },
    'saturday': {
        'start': '10:30',
        'end': '15:30'
    }
}

def generate_available_hours(start_date: datetime = None) -> Dict[str, List[Dict[str, str]]]:
    """
    Generate available hours for the next 14 days based on the configured schedule.
    Weekdays: 10:00-19:00 (Mexico City time)
    Saturday: 10:30-15:30 (Mexico City time)
    Sunday: Closed
    
    Args:
        start_date: Optional start date. If not provided, uses current date.
    
    Returns:
        Dictionary with dates as keys and lists of time slots as values.
    """
    # Get current date if no start date provided
    current_date = start_date or datetime.now(pytz.UTC)
    
    # Get events for the next 15 days
    events = get_events(current_date, current_date + timedelta(days=15))
    
    # Initialize response dictionary
    schedule = {}
    
    # Get Mexico City timezone
    mexico_tz = pytz.timezone('America/Mexico_City')
    
    # Generate data for current week and next week (14 days)
    for day_offset in range(14):
        current_day = current_date + timedelta(days=day_offset)
        
        # Skip Sundays (6 is Sunday)
        if current_day.weekday() == 6:
            continue
            
        date_str = current_day.strftime("%Y-%m-%d")
        schedule[date_str] = []
        
        # Get schedule based on day type
        if current_day.weekday() == 5:  # Saturday
            day_schedule = SCHEDULE['saturday']
        else:  # Weekday
            day_schedule = SCHEDULE['weekday']
            
        # Parse start and end times
        start_hour, start_minute = map(int, day_schedule['start'].split(':'))
        end_hour, end_minute = map(int, day_schedule['end'].split(':'))
        
        # Convert current day to Mexico City time for schedule
        current_day_mx = current_day.astimezone(mexico_tz)
        
        # Set time blocks in Mexico City time
        block_start = current_day_mx.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
        block_end = current_day_mx.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
        
        # Add 15-minute intervals
        current_time = block_start
        while current_time < block_end:
            next_time = current_time + timedelta(minutes=15)
            
            # Check if this time block overlaps with any existing event
            is_available = True
            for event in events:
                event_start = datetime.fromisoformat(event['start'].replace('Z', '+00:00'))
                event_end = datetime.fromisoformat(event['end'].replace('Z', '+00:00'))
                
                # Convert event times to Mexico City time for comparison
                event_start_mx = event_start.astimezone(mexico_tz)
                event_end_mx = event_end.astimezone(mexico_tz)
                
                # Check for overlap
                if (current_time < event_end_mx and next_time > event_start_mx):
                    print(f"Event {event['name']} overlaps with time block {current_time} - {next_time}")
                    is_available = False
                    break
            
            if is_available:
                # Convert back to UTC for the response
                current_time_utc = current_time.astimezone(pytz.UTC)
                next_time_utc = next_time.astimezone(pytz.UTC)
                
                schedule[date_str].append({
                    "from": current_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "to": next_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
                })
            
            current_time = next_time
    
    return schedule 