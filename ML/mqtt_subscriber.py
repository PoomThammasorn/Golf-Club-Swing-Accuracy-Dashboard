import os
import json
import base64
import cv2
import numpy as np
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Initialize last_frame to None
last_frame = None


def on_message(client, userdata, message):
    global last_frame
    try:
        # Decode the incoming MQTT message payload from bytes to string
        payload_str = message.payload.decode('utf-8')
        # Parse the JSON object to get the base64-encoded frame
        payload = json.loads(payload_str)
        if "data" not in payload:
            print("Error: 'data' field not found in the message payload.")
            return
        # Extract the base64-encoded image from the "data" field
        jpg_as_text = payload["data"]
        # Decode the base64-encoded image back to binary data
        frame_data = base64.b64decode(jpg_as_text)
        # Convert the binary image data into a numpy array
        np_arr = np.frombuffer(frame_data, np.uint8)
        # Decode the numpy array into an image (OpenCV format)
        last_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if last_frame is not None:
            # Display the frame using OpenCV
            cv2.imshow('Received Frame', last_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return  # Close window on pressing 'q'

    except Exception as e:
        print(f"Error processing frame: {e}")


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
    # Load environment variables
    load_dotenv("./configs/.env")

    # Start the MQTT client in a separate thread
    start_mqtt_thread()

    # Start displaying the video stream
    show_video()


if __name__ == "__main__":
    main()
