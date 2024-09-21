import paho.mqtt.client as mqtt
import json
import random
import time
import os
from dotenv import load_dotenv


def load_environment_variables():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(BASE_DIR, "../.."))
    load_dotenv(os.path.join(project_root, "IoT/mqtt/configs/.env"))


def generate_sensor_data():
    return {
        'accelerometer': {
            'x': round(random.uniform(-10, 10), 2),
            'y': round(random.uniform(-10, 10), 2),
            'z': round(random.uniform(-10, 10), 2)
        },
        'gyroscope': {
            'x': round(random.uniform(0, 360), 2),
            'y': round(random.uniform(0, 360), 2),
            'z': round(random.uniform(0, 360), 2)
        }
    }


def setup_mqtt_client():
    broker_address = os.getenv("MQTT_URL", "localhost")
    broker_port = int(os.getenv("MQTT_PORT", 1883))

    client = mqtt.Client()
    client.connect(broker_address, broker_port, 60)
    return client


def publish_sensor_data(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"Published to {topic}: {data}")


def run_sensor_publisher():
    load_environment_variables()
    client = setup_mqtt_client()
    topic_sensor = os.getenv("MQTT_SENSORS_TOPIC", "sensors/data")

    # Start MQTT loop for handling communication
    client.loop_start()

    try:
        while True:
            sensor_data = generate_sensor_data()
            publish_sensor_data(client, topic_sensor, sensor_data)
            time.sleep(1)  # Delay between each data publish
    except KeyboardInterrupt:
        print("Stopping sensor data publisher...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run_sensor_publisher()
