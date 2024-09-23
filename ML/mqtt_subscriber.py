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
        # Decode the incoming MQTT message payload
        payload_str = message.payload.decode('utf-8')
        # Parse the JSON object
        payload = json.loads(payload_str)

        # Check if "data" field exists
        if "data" not in payload:
            print("Error: 'data' field not found in the message payload.")
            return

        # Extract and decode the base64-encoded frame
        jpg_as_text = payload["data"]
        frame_data = base64.b64decode(jpg_as_text)

        # Convert the binary data to a numpy array
        np_arr = np.frombuffer(frame_data, np.uint8)
        last_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"Error processing frame: {e}")


def setup_mqtt_client():
    print("Setting up MQTT client...")

    broker_address = os.getenv("MQTT_URL", "localhost")
    broker_port = int(os.getenv("MQTT_PORT", 1883))
    topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")

    client = mqtt.Client()
    client.on_message = on_message

    client.connect(broker_address, broker_port, 60)
    client.subscribe(topic)
    print(f"Subscribed to {topic}")

    # Start the MQTT loop
    client.loop_start()


def start_mqtt_thread():
    mqtt_thread = threading.Thread(target=setup_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()


def show_video():
    global last_frame
    while True:
        if last_frame is not None:
            cv2.imshow('MQTT Camera Feed', last_frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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
