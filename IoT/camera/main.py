import cv2
from mqtt.mqtt_setup import setup_mqtt_client, publish_data
import base64
from dotenv import load_dotenv
import os
import time


def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"


def publish_frames_to_mqtt(client, mqtt_topic, rtsp_url):
    while True:
        cap = cv2.VideoCapture(rtsp_url)

        if not cap.isOpened():
            print("Error: Could not open video stream. Retrying...")
            time.sleep(5)  # Wait before retrying
            continue  # Retry connection

        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Error: Could not read frame. Reconnecting...")
                    break  # Break to reconnect

                # Encode the frame to JPEG format and convert to base64
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer)
                # Prepare the data to be published
                data = {"data": jpg_as_text}
                # Publish the frame to the MQTT topic
                publish_data(client, mqtt_topic, data)
                print(f"Published frame to {mqtt_topic}")

        except KeyboardInterrupt:
            print("Interrupted by user.")
            break
        finally:
            cap.release()
            print("Released video capture. Reconnecting...")


def main():
    load_dotenv("./configs/.env")

    mqtt_client = setup_mqtt_client(
        broker_address=os.getenv("MQTT_BROKER_ADDRESS"),
        broker_port=int(os.getenv("MQTT_BROKER_PORT"))
    )
    mqtt_topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")
    rtsp_url = get_rtsp_url()

    publish_frames_to_mqtt(mqtt_client, mqtt_topic, rtsp_url)

    mqtt_client.disconnect()
    print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()
