from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Dict, List

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/available-hours")
async def get_available_hours():
    # Get current date
    current_date = datetime.now()
    
    # Initialize response dictionary
    available_hours = {}
    
    # Generate data for current week and next week (14 days)
    for day_offset in range(14):
        current_day = current_date + timedelta(days=day_offset)
        
        # Skip weekends (5 is Saturday, 6 is Sunday)
        if current_day.weekday() >= 5:
            continue
            
        date_str = current_day.strftime("%Y-%m-%d")
        available_hours[date_str] = []
        
        # Add two time blocks for each weekday
        # Morning block: 9:00-10:00
        morning_start = current_day.replace(hour=9, minute=0, second=0, microsecond=0)
        morning_end = current_day.replace(hour=10, minute=0, second=0, microsecond=0)
        
        # Afternoon block: 14:00-15:00
        afternoon_start = current_day.replace(hour=14, minute=0, second=0, microsecond=0)
        afternoon_end = current_day.replace(hour=15, minute=0, second=0, microsecond=0)
        
        # Add 15-minute intervals for morning block
        current_time = morning_start
        while current_time < morning_end:
            next_time = current_time + timedelta(minutes=15)
            available_hours[date_str].append({
                "from": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "to": next_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
            current_time = next_time
            
        # Add 15-minute intervals for afternoon block
        current_time = afternoon_start
        while current_time < afternoon_end:
            next_time = current_time + timedelta(minutes=15)
            available_hours[date_str].append({
                "from": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "to": next_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
            current_time = next_time
    
    return available_hours

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 