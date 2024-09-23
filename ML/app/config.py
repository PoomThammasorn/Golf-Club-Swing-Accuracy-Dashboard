import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("./configs/.env")


class Settings:
    NODE_WEBHOOK_URL: str = os.getenv("NODE_WEBHOOK_URL", "http://localhost:8000")
    PORT: int = int(os.getenv("PORT", 9000))


# Instantiate settings
settings = Settings()
