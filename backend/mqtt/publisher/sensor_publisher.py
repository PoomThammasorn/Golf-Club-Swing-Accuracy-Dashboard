import paho.mqtt.client as mqtt
import json
import time
import random
import mpu6050
import sys
import logging

mpu6050 = mpu6050.mpu6050(0x68)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_sensor_data():
    accel_data = mpu6050.get_accel_data()
    gyro_data = mpu6050.get_gyro_data()

    return {
        "accelerometer": accel_data,
        "gyroscope": gyro_data
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to broker successfully")
    else:
        logger.error("Connection failed with code: %s", rc)

def on_publish(client, userdata, mid):
    logger.info("Message %s published", mid)

def main(broker_ip):
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(broker_ip, 1883, 60)
    client.loop_start()

    try:
        while True:
            sensor_data = read_sensor_data()
            client.publish("sensor/data", json.dumps(sensor_data))
            time.sleep(0.1)  # Adjust as needed
    except KeyboardInterrupt:
        logger.info("Exiting...")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logger.error("Usage: python3 publisher.py <broker_ip>")
        sys.exit(1)
    else:
        broker_ip = sys.argv[1]
        main(broker_ip)
