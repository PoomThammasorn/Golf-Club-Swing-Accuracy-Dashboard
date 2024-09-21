from fastapi import FastAPI
from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import threading

# Load environment variables from .env file
load_dotenv("configs/.env")

# Initialize FastAPI app
app = FastAPI()

# Global variable to store the last received message
last_message = None

# Define the MQTT broker address and topic
broker_address = "localhost"
topic = "sensor/data"

# Callback function when a message is received


def on_message(client, userdata, message):
    global last_message
    last_message = message.payload.decode()  # Decode the message
    print(f"Received message: {last_message} on topic: {message.topic}")

# Function to set up the MQTT client


def setup_mqtt_client():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address)
    client.subscribe(topic)
    client.loop_start()  # Start the loop to process network traffic and callbacks


# Start the MQTT client in a separate thread
mqtt_thread = threading.Thread(target=setup_mqtt_client)
mqtt_thread.start()


@app.get("/")
async def root():
    return {"message": "Server is running"}


@app.get("/last_message")
async def get_last_message():
    return {"last_message": last_message}

# Run the app with the port from .env
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 9000))
    uvicorn.run(app, port=port)
