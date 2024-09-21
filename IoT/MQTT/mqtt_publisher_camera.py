import cv2
import paho.mqtt.client as mqtt
import base64
from dotenv import load_dotenv
import os


def load_environment_variables():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(BASE_DIR, "../.."))
    load_dotenv(os.path.join(project_root, "IoT/mqtt/configs/.env"))


def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"


def initialize_mqtt_client():
    mqtt_broker = os.getenv("MQTT_URL", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    return client


def publish_frames_to_mqtt(client, mqtt_topic, rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Encode the frame to JPEG format and convert to base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)

            # Publish the frame to the MQTT topic
            client.publish(mqtt_topic, jpg_as_text)
            print(f"Published frame to {mqtt_topic}")

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()


def main():
    load_environment_variables()

    mqtt_client = initialize_mqtt_client()
    mqtt_topic = os.getenv("MQTT_CAMERA_TOPIC", "camera/data")
    rtsp_url = get_rtsp_url()

    publish_frames_to_mqtt(mqtt_client, mqtt_topic, rtsp_url)

    mqtt_client.disconnect()
    print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()
