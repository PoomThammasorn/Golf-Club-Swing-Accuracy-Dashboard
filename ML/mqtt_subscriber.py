import os
import json
import base64
import cv2
import numpy as np
import threading
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from threading import Lock
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Thread lock for handling frame access
frame_lock = Lock()
last_frame = None  # Shared frame across threads


def on_message(client, userdata, message):
    global last_frame
    try:
        payload_str = message.payload.decode("utf-8")
        payload = json.loads(payload_str)

        if "data" not in payload:
            logging.error("Error: 'data' field not found in the message payload.")
            return

        jpg_as_text = payload["data"]
        frame_data = base64.b64decode(jpg_as_text)
        np_arr = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None:
            with frame_lock:
                last_frame = frame
        else:
            logging.error("Error: Could not decode image data.")

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
    except Exception as e:
        logging.error(f"Error processing frame: {e}")


def setup_mqtt_client(broker_address, broker_port, topic):
    logging.info("Setting up MQTT client...")

    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect(broker_address, broker_port, 60)
        client.subscribe(topic)
        logging.info(f"Subscribed to {topic}")

        # Start the MQTT loop
        client.loop_start()
    except Exception as e:
        logging.error(f"Error connecting to MQTT broker: {e}")


def start_mqtt_thread(broker_address, broker_port, topic):
    mqtt_thread = threading.Thread(
        target=setup_mqtt_client, args=(broker_address, broker_port, topic)
    )
    mqtt_thread.daemon = True
    mqtt_thread.start()


def show_video(fps=30):
    global last_frame
    delay = int(1000 / fps)
    while True:
        with frame_lock:
            if last_frame is not None:
                cv2.imshow("MQTT Camera Feed", last_frame)

        if cv2.waitKey(delay) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    logging.info("Video feed closed.")


def main():
    load_dotenv("./configs/.env")
    broker_address = os.getenv("MQTT_URL", "localhost")
    broker_port = int(os.getenv("MQTT_PORT", 1883))
    topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")

    try:
        start_mqtt_thread(broker_address, broker_port, topic)
        show_video(fps=30)
    except KeyboardInterrupt:
        logging.info("Exiting...")


if __name__ == "__main__":
    main()
