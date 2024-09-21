import os
import base64
import cv2
import numpy as np
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Global variable to store the last received image
global last_frame


def load_environment_variables():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    # Load MQTT and ML configuration files
    load_dotenv(os.path.join(project_root, "configs/mqtt.env"))
    load_dotenv(os.path.join(project_root, "ML/configs/.env"))


def on_message(client, userdata, message):
    global last_frame
    # Decode the base64 message back to an image format
    frame_data = base64.b64decode(message.payload)
    np_arr = np.frombuffer(frame_data, np.uint8)
    last_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def setup_mqtt_client():
    print("Setting up MQTT client...")

    # Define the MQTT broker address and topic from environment variables
    broker_address = os.getenv("MQTT_URL")
    # Default to 1883 if not set
    broker_port = int(os.getenv("MQTT_PORT", 1883))
    topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")  # Default topic

    client = mqtt.Client()
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_address, broker_port, 60)

    # Subscribe to the specified topic
    client.subscribe(topic)
    print(f"Subscribed to {topic}")

    # Start the MQTT loop in a separate thread
    client.loop_start()


def start_mqtt_thread():
    mqtt_thread = threading.Thread(target=setup_mqtt_client)
    mqtt_thread.daemon = True  # Ensure thread exits when the main program exits
    mqtt_thread.start()


def show_video():
    global last_frame
    while True:
        if last_frame is not None:
            # Display the frame in an OpenCV window
            cv2.imshow('MQTT Camera Feed', last_frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the OpenCV window
    cv2.destroyAllWindows()


def main():
    last_frame = None
    # Load environment variables
    load_environment_variables()

    # Start the MQTT client in a separate thread
    start_mqtt_thread()

    # Start displaying the video stream
    show_video()


if __name__ == "__main__":
    main()
