# mqtt_setup.py
import paho.mqtt.client as mqtt
import json
import time
import logging


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info(f"Connected to MQTT Broker successfully.")
    else:
        logging.error(f"Failed to connect, return code {rc}")


def on_publish(client, userdata, mid):
    logging.info(f"Message {mid} published.")


class MQTTClient:
    def __init__(self, broker_address, broker_port, keep_alive=60):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.keep_alive = keep_alive

    def connect(self):
        logging.info(
            f"Connecting to MQTT Broker at {self.broker_address}:{self.broker_port}"
        )
        self.client.connect(self.broker_address, self.broker_port, self.keep_alive)
        self.client.loop_start()

    def publish(self, topic, data):
        payload = json.dumps(data)
        self.client.publish(topic, payload)
        logging.info(f"Published to {topic} at {time.time():.2f}")
