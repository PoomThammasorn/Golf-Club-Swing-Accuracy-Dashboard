from fastapi import FastAPI
from dotenv import load_dotenv
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, ".."))
load_dotenv(os.path.join(project_root, "ML/configs/.env"))


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
