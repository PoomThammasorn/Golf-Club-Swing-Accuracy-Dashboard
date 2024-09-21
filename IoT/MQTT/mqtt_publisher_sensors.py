import paho.mqtt.client as mqtt  # type: ignore
import json
import random
import time

# Function to generate random sensor data for accelerometer and gyroscope


def get_sensor_data():
    accelerometer = {
        'x': round(random.uniform(-10, 10), 2),
        'y': round(random.uniform(-10, 10), 2),
        'z': round(random.uniform(-10, 10), 2)
    }
    gyroscope = {
        'x': round(random.uniform(0, 360), 2),
        'y': round(random.uniform(0, 360), 2),
        'z': round(random.uniform(0, 360), 2)
    }
    return {
        'accelerometer': accelerometer,
        'gyroscope': gyroscope
    }


# Define the MQTT broker address and topics
broker_address = "localhost"
topic_sensor = "sensor/data"

# Create a new MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address)

# Start the loop to process callbacks
client.loop_start()

try:
    while True:
        # Generate sensor data
        sensor_data = get_sensor_data()

        # Publish the data to the respective MQTT topics
        client.publish(topic_sensor, json.dumps(sensor_data))

        print(f"Published to {topic_sensor}: {sensor_data}")
        # Wait for 1 second before sending the next data
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the loop and disconnect on interrupt
    print("Stopping sensor data publisher...")
    client.loop_stop()
    client.disconnect()
