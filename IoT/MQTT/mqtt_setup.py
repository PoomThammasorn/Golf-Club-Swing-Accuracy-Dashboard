# mqtt_setup.py
import paho.mqtt.client as mqtt
import json
import time


def setup_mqtt_client(broker_address, broker_port):

    client = mqtt.Client()
    client.connect(broker_address, broker_port, 60)
    return client


def publish_data(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)
    print(f"Published to {topic} at {time.time()}")
