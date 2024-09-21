import cv2
import paho.mqtt.client as mqtt
import base64

# MQTT broker information
mqtt_broker = "localhost"  # Replace with your MQTT broker IP or hostname
mqtt_port = 1883
mqtt_topic = "camera/data"  # MQTT topic to publish frames to

# Your IP camera's RTSP URL
rtsp_url = "rtsp://admin:admin@10.78.126.72:8554/live"

# Initialize MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
else:
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Encode the frame to JPEG format and convert to base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)

            # Publish the frame to the MQTT topic
            client.publish(mqtt_topic, jpg_as_text)
            print(f"Published frame to {mqtt_topic}")

    except KeyboardInterrupt:
        print("Interrupted by user.")
        print("Closing the connection...")

# Release the capture
cap.release()
cv2.destroyAllWindows()

# Disconnect from the MQTT broker
client.disconnect()
