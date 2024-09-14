from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("configs/.env")

# Initialize FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "server is running"}

# Run the app with the port from .env
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 9000))
    uvicorn.run(app,  port=port)
