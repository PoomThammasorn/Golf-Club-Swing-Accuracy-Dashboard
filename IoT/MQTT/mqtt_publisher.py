import paho.mqtt.client as mqtt  # type: ignore
import json
import random
import time

# Function to generate random sensor data


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


# Define the MQTT broker address and topic
broker_address = "localhost"
topic = "sensor/data"

# Create a new MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address)

# Start the loop to process callbacks
client.loop_start()

try:
    while True:
        # Generate sensor data
        data = get_sensor_data()
        message = json.dumps(data)

        # Publish the data to the MQTT topic
        client.publish(topic, message)
        print(f"Published: {message}")

        # Wait for 1 second before sending the next data
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the loop and disconnect on interrupt
    print("Stopping sensor data publisher...")
    client.loop_stop()
    client.disconnect()
