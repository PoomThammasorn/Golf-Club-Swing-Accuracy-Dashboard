from fastapi import FastAPI
from app.routes import ml
from app.config import settings


# Initialize FastAPI app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "server is running"}


# Include the router for ML-related routes
app.include_router(ml.router)

# Run the app with the port from .env
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=settings.PORT)
