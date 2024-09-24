import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("./configs/.env")


class Settings:
    NODE_WEBHOOK_URL: str = os.getenv("NODE_WEBHOOK_URL", "http://localhost:8000")
    PORT: int = int(os.getenv("PORT", 9000))
    MQTT_URL: str = os.getenv("MQTT_URL", "localhost")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 1883))
    MQTT_CAMERA_TOPIC: str = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")
    MQTT_SENSORS_TOPIC: str = os.getenv("MQTT_SENSORS_TOPIC", "sensors/data")


# Instantiate settings
settings = Settings()
