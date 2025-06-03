from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.available_hours import generate_available_hours

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
    return generate_available_hours()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 