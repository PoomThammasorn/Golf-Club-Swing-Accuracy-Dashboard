import paho.mqtt.client as mqtt
import cv2
import json
import time

# Define MQTT broker address and topic
broker_address = "localhost"
topic_camera = "camera/data"

# Create a new MQTT client instance
client = mqtt.Client()
client.connect(broker_address)
client.loop_start()

# Connect to the IP camera stream
rtsp_url = "rtsp://username:password@camera_ip_address/stream"
cap = cv2.VideoCapture(rtsp_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame (for example, take a snapshot)
    _, buffer = cv2.imencode('.jpg', frame)
    image_data = buffer.tobytes()

    # Optionally convert image to base64 for transmission
    # import base64
    # image_base64 = base64.b64encode(image_data).decode('utf-8')
    # message = json.dumps({"image_data": image_base64, "timestamp": time.time()})

    # Publish the image data to the MQTT topic
    client.publish(topic_camera, image_data)  # Sending raw image data
    print("Published camera data")

    # Wait for a bit before sending the next frame
    time.sleep(1)

cap.release()
client.loop_stop()
client.disconnect()
