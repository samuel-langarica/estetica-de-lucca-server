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
    # Sample data for demonstration with 15-minute blocks
    sample_data = {
        "2024-03-20": [
            {
                "from": "2024-03-20T09:00:00Z",
                "to": "2024-03-20T09:15:00Z"
            },
            {
                "from": "2024-03-20T09:15:00Z",
                "to": "2024-03-20T09:30:00Z"
            },
            {
                "from": "2024-03-20T09:30:00Z",
                "to": "2024-03-20T09:45:00Z"
            },
            {
                "from": "2024-03-20T09:45:00Z",
                "to": "2024-03-20T10:00:00Z"
            },
            {
                "from": "2024-03-20T14:00:00Z",
                "to": "2024-03-20T14:15:00Z"
            },
            {
                "from": "2024-03-20T14:15:00Z",
                "to": "2024-03-20T14:30:00Z"
            },
            {
                "from": "2024-03-20T14:30:00Z",
                "to": "2024-03-20T14:45:00Z"
            },
            {
                "from": "2024-03-20T14:45:00Z",
                "to": "2024-03-20T15:00:00Z"
            }
        ],
        "2024-03-21": [
            {
                "from": "2024-03-21T10:00:00Z",
                "to": "2024-03-21T10:15:00Z"
            },
            {
                "from": "2024-03-21T10:15:00Z",
                "to": "2024-03-21T10:30:00Z"
            },
            {
                "from": "2024-03-21T10:30:00Z",
                "to": "2024-03-21T10:45:00Z"
            },
            {
                "from": "2024-03-21T10:45:00Z",
                "to": "2024-03-21T11:00:00Z"
            },
            {
                "from": "2024-03-21T15:00:00Z",
                "to": "2024-03-21T15:15:00Z"
            },
            {
                "from": "2024-03-21T15:15:00Z",
                "to": "2024-03-21T15:30:00Z"
            },
            {
                "from": "2024-03-21T15:30:00Z",
                "to": "2024-03-21T15:45:00Z"
            },
            {
                "from": "2024-03-21T15:45:00Z",
                "to": "2024-03-21T16:00:00Z"
            }
        ]
    }
    
    return sample_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 