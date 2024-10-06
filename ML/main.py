import cv2
import os
import time
import logging
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from services.frame_storage import FrameStorage
from model.detection import Detection
import threading
import time
import logging
import queue
import warnings
import uvicorn
from services.mqtt import MQTTClient


warnings.filterwarnings("ignore")

load_dotenv("./configs/.env")

# Set up logging
logging.basicConfig(level=logging.INFO)

frame_storage = FrameStorage(buffer_size=100)

detection = Detection()

mqtt = MQTTClient(
    broker_address=os.getenv("MQTT_URL", "localhost"),
    broker_port=int(os.getenv("MQTT_PORT", 1883)),
    keep_alive=60,
)

app = FastAPI()


def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP", "localhost")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"


def process_frames_with_ml(frame):
    # Replace with your actual ML processing logic
    # datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(frame["timestamp"]))
    # logging.info(f"Processing frame at timestamp: {datetime}")
    # save the frame to file
    path = f"frames/frame_{frame['timestamp']}.jpg"
    with open(path, "wb") as f:
        f.write(frame["data"])
    # Example: ML processing logic here
    # Check if the file was saved
    if os.path.exists(path):
        # Call ML processing
        try:
            result = detection.predict(path)
            logging.info("ML processing complete.")
            return result
        except Exception as e:
            os.remove(path)
            logging.error("Failed to process frame")
    else:
        logging.error(f"Failed to save the frame to {path}")
    return None


def async_ml_processing(process_frames_with_ml, time_stamp=None):
    # Get buffered frames and clear the buffer
    frame = frame_storage.get_frame_by_timestamp(time_stamp)

    if frame is None:
        logging.error("Error: No frame found in the buffer.")
        return None  # No frame found

    # Create a queue to store the result
    result_queue = queue.Queue()

    # Run the ML processing in a new thread
    def ml_process():
        result = process_frames_with_ml(frame)
        result_queue.put(result)  # Store the result in the queue

    processing_thread = threading.Thread(target=ml_process)
    processing_thread.start()
    processing_thread.join()  # Wait for the thread to finish

    # Retrieve the result from the queue
    result = result_queue.get()
    return result


def capture_and_store_frames(rtsp_url):
    retry_count = 0
    max_retries = 5
    base_delay = 5  # Base delay for exponential backoff

    while retry_count < max_retries:
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            retry_count += 1
            delay = base_delay * retry_count
            logging.error(
                f"Error: Could not open video stream. Retrying {retry_count}/{max_retries} in {delay} seconds..."
            )
            time.sleep(delay)
            continue  # Retry connection

        logging.info("Successfully opened video stream.")
        retry_count = 0  # Reset on successful connection
        frame_storage.clear_buffer()
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logging.error("Error: Could not read frame. Reconnecting...")
                    break  # Break to reconnect
                # Encode the frame to JPEG format with full quality and store in buffer
                _, buffer = cv2.imencode(
                    ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100]
                )
                frame_storage.store_frame(buffer)

        except KeyboardInterrupt:
            logging.info("Process interrupted by user.")
            break
        except Exception as e:
            logging.error(f"Error during frame capture: {e}")
            break  # Handle any other errors and attempt reconnection
        finally:
            cap.release()
            frame_storage.clear_buffer()
            logging.info("Released video capture. Reconnecting...")


@app.post("/ml")
async def trigger_ml(request: dict):
    timestamp = request.get("timestamp", None)
    if frame_storage.get_buffer_size() == 0:
        raise HTTPException(status_code=404, detail="No frames available in buffer.")

    # Trigger ML processing
    result = async_ml_processing(process_frames_with_ml, timestamp)
    if result is None:
        raise HTTPException(status_code=500, detail="Error processing frame.")
    else:
        mqtt.publish("ml/data", {"timestamp": timestamp, "result": result})
        return {"message": "ML processing complete."}


def main():
    rtsp_url = get_rtsp_url()
    logging.info(f"RTSP URL: {rtsp_url}")
    logging.info("Capturing frames and waiting for ML trigger.")

    mqtt.connect()

    # Start capturing frames in the background
    capture_thread = threading.Thread(target=capture_and_store_frames, args=(rtsp_url,))
    capture_thread.start()


if __name__ == "__main__":
    main()
    uvicorn.run(app, host="localhost", port=9000)
