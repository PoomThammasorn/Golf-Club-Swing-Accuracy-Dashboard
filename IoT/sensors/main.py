# main.py
import time
from mqtt.mqtt_setup import setup_mqtt_client, publish_data
import os
from dotenv import load_dotenv
from mpu6050 import mpu6050
from time import sleep


def run_sensor_publisher():
    load_dotenv("./configs/.env")
    client = setup_mqtt_client(
        broker_address=os.getenv("MQTT_URL", "localhost"),
        broker_port=int(os.getenv("MQTT_PORT", 1883))
    )
    topic_sensor = os.getenv("MQTT_SENSORS_TOPIC", "sensors/data")

    # Start MQTT loop for handling communication
    client.loop_start()
    sensor = mpu6050(0x68)
    try:
        while True:
            # Retrieve accelerometer data from the sensor.
            accel_data = sensor.get_accel_data()
            # Retrieve gyroscope data from the sensor.
            gyro_data = sensor.get_gyro_data()
            sensor_data = {
                "data": {
                    "accelerometer": accel_data,
                    "gyroscope": gyro_data
                }
            }
            publish_data(client, topic_sensor, sensor_data)
            time.sleep(0.01)  # Sent data every ~10ms
    except KeyboardInterrupt:
        print("Stopping sensor data publisher...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run_sensor_publisher()
