import paho.mqtt.client as mqtt
import json
import time
import random

def main(broker_ip="localhost"):
    client = mqtt.Client()
    client.connect(broker_ip, 1883, 60)
    client.loop_start()

    while True:
        client.publish("camera/video", json.dumps({"frame": random.randint(0, 100)}))
        time.sleep(0.1)  # Adjust as needed

main()
