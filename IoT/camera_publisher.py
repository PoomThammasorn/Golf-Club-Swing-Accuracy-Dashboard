import cv2
from mqtt.mqtt_setup import (
    setup_mqtt_client,
    publish_data,
)
import base64
from dotenv import load_dotenv
import os
import time
import logging
from collections import deque

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP", "localhost")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"

def publish_buffered_frames(client, mqtt_topic, buffer):
    """Publish all frames in the buffer to the MQTT topic."""
    while buffer:
        frame = buffer.popleft()  # Get the oldest frame
        publish_data(client, mqtt_topic, frame)  # Publish frame data

def publish_frames_to_mqtt(client, mqtt_topic, rtsp_url, buffer_size=10):
    retry_count = 0
    max_retries = 5
    base_delay = 5  # Base delay for exponential backoff
    frame_buffer = deque(maxlen=buffer_size)  # Buffer to store frames

    while retry_count < max_retries:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            retry_count += 1
            delay = base_delay * retry_count
            logging.error(
                f"Error: Could not open video stream. Retrying {retry_count}/{max_retries} in {delay} seconds..."
            )
            time.sleep(delay)
            continue  # Retry connection

        logging.info("Successfully opened video stream.")
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

                # Add the frame data to the buffer
                frame_buffer.append(data)

                # If buffer is full, publish all frames in the buffer
                if len(frame_buffer) >= buffer_size:
                    logging.info(f"Buffer full. Publishing {buffer_size} frames.")
                    publish_buffered_frames(client, mqtt_topic, frame_buffer)

        except KeyboardInterrupt:
            logging.info("Process interrupted by user.")
            break
        except Exception as e:
            logging.error(f"Error during frame publishing: {e}")
            break  # Handle any other errors and attempt reconnection
        finally:
            cap.release()
            logging.info("Released video capture. Reconnecting...")

    # If any frames remain in the buffer, publish them before exiting
    if frame_buffer:
        logging.info(f"Publishing remaining {len(frame_buffer)} frames before exiting.")
        publish_buffered_frames(client, mqtt_topic, frame_buffer)

    logging.error("Max retries reached. Exiting...")

def main():
    load_dotenv("./configs/.env")

    # Ensure all necessary environment variables are set
    required_vars = ["MQTT_URL", "MQTT_PORT", "MQTT_CAMERA_TOPIC", "RSTP_USER", "RSTP_PASSWORD", "RSTP_IP", "RSTP_PORT", "RSTP_PATH"]
    missing_vars = [var for var in required_vars if os.getenv(var) is None]

    if missing_vars:
        logging.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return

    try:
        mqtt_client = setup_mqtt_client(
            broker_address=os.getenv("MQTT_URL", "localhost"),
            broker_port=int(os.getenv("MQTT_PORT", 1883)),
            keep_alive=60,
        )
        logging.info("MQTT client setup successfully.")
    except Exception as e:
        logging.error(f"Error setting up MQTT client: {e}")
        return

    mqtt_topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")
    rtsp_url = get_rtsp_url()

    logging.info(f"RTSP URL: {rtsp_url}")
    logging.info(f"Publishing frames to MQTT topic: {mqtt_topic}")

    try:
        publish_frames_to_mqtt(mqtt_client, mqtt_topic, rtsp_url, buffer_size=10)  # Set buffer size here
    except Exception as e:
        logging.error(f"An error occurred during the publishing process: {e}")
    finally:
        mqtt_client.disconnect()
        logging.info("Disconnected from MQTT broker.")

if __name__ == "__main__":
    main()
