import cv2
from mqtt.mqtt_setup import (
    setup_mqtt_client,
    publish_data,
)  # Assuming mqtt_setup.py is configured properly
import base64
from dotenv import load_dotenv
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP", "localhost")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"


def publish_frames_to_mqtt(client, mqtt_topic, rtsp_url):
    retry_count = 0
    max_retries = 5
    while retry_count < max_retries:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            retry_count += 1
            logging.error(
                f"Error: Could not open video stream. Retrying {retry_count}/{max_retries}..."
            )
            time.sleep(5)
            continue  # Retry connection
        retry_count = 0  # Reset on successful connection
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logging.error("Error: Could not read frame. Reconnecting...")
                    break  # Break to reconnect
                # Encode the frame to JPEG format and convert to base64
                _, buffer = cv2.imencode(
                    ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80]
                )  # Compress with 80% quality
                jpg_as_text = base64.b64encode(buffer).decode("utf-8")
                # Prepare the data to be published
                data = {"data": jpg_as_text}
                # Publish the frame to the MQTT topic
                publish_data(client, mqtt_topic, data)
        except KeyboardInterrupt:
            logging.info("Interrupted by user.")
            break
        finally:
            cap.release()
            logging.info("Released video capture. Reconnecting...")
    logging.error("Max retries reached. Exiting...")


def main():
    load_dotenv("./configs/.env")
    try:
        mqtt_client = setup_mqtt_client(
            broker_address=os.getenv("MQTT_URL", "localhost"),
            broker_port=int(os.getenv("MQTT_PORT", 1883)),
            keep_alive=60,
        )
    except Exception as e:
        logging.error(f"Error setting up MQTT client: {e}")
        return

    mqtt_topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")
    rtsp_url = get_rtsp_url()

    publish_frames_to_mqtt(mqtt_client, mqtt_topic, rtsp_url)

    mqtt_client.disconnect()
    logging.info("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()
