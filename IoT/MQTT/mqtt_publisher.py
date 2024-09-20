import paho.mqtt.client as mqtt
import json
from sensors.mpu6050_reader import get_sensor_data

# Load MQTT configuration
broker_address = "YOUR_COMPUTER_IP_ADDRESS"
topic = "sensor/data"

def publish_sensor_data():
    client = mqtt.Client()
    client.connect(broker_address)
    
    sensor_data = get_sensor_data()
    payload = json.dumps(sensor_data)
    
    client.publish(topic, payload)
    print(f"Published: {payload}")

if __name__ == "__main__":
    publish_sensor_data()
