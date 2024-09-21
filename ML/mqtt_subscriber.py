from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import threading
import base64
import cv2
import numpy as np

# Load environment variables from .env file
load_dotenv("../configs/mqtt.env")

# Global variable to store the last received image
last_frame = None

# Define the MQTT broker address and topic
broker_address = os.getenv("MQTT_URL")
broker_port = int(os.getenv("MQTT_PORT"))
topic = os.getenv("MQTT_CAMERA_TOPIC")

# Callback function when a message is received


def on_message(client, userdata, message):
    global last_frame
    # Decode the base64 message back to image format
    frame_data = base64.b64decode(message.payload)
    np_arr = np.frombuffer(frame_data, np.uint8)
    last_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# Function to set up the MQTT client


def setup_mqtt_client():
    print("Setting up MQTT client...")
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port, 60)
    client.subscribe(topic)
    print(f"Subscribed to {topic}")
    client.loop_start()  # Start the loop to process network traffic and callbacks


# Start the MQTT client in a separate thread
mqtt_thread = threading.Thread(target=setup_mqtt_client)
mqtt_thread.start()

# Function to display the video stream using OpenCV


def show_video():
    global last_frame
    while True:
        if last_frame is not None:
            # Display the frame in an OpenCV window
            cv2.imshow('MQTT Camera Feed', last_frame)

        # Add a small delay for smoother playback and wait for 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the window when done
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Start the video display in the main thread
    show_video()
