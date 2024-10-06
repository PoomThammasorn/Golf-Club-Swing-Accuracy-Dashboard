import cv2
import base64
from dotenv import load_dotenv
import os
import time
import logging
import threading
from frame_storage import FrameStorage  # Import your FrameStorage class

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_rtsp_url():
    rstp_user = os.getenv("RSTP_USER", "admin")
    rstp_password = os.getenv("RSTP_PASSWORD", "admin")
    rstp_ip = os.getenv("RSTP_IP", "localhost")
    rstp_port = os.getenv("RSTP_PORT", "8554")
    rstp_path = os.getenv("RSTP_PATH", "live")
    return f"rtsp://{rstp_user}:{rstp_password}@{rstp_ip}:{rstp_port}/{rstp_path}"


def process_frames_with_ml(frame):
    # Replace with your actual ML processing logic
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(frame["timestamp"]))
    logging.info(f"Processing frame at timestamp: {datetime}")
    # save the frame to file
    with open(f"frames/frame_{frame['timestamp']}.jpg", "wb") as f:
        f.write(frame["data"])
    # Example: ML processing logic here
    time.sleep(2)  # Simulate ML processing time
    logging.info("ML processing complete.")


def async_ml_processing(frame_storage: FrameStorage, process_frames_with_ml):

    # Get buffered frames and clear the buffer at the same time
    frame = frame_storage.get_frame_by_timestamp(time.time() - 1, tolerance=10)

    if frame is None:
        logging.error("Error: No frame found in the buffer.")
        return

    # Run the ML processing in a new thread
    def ml_process():
        process_frames_with_ml(frame)  # Call ML processing function
        logging.info("ML processing complete.")

    processing_thread = threading.Thread(target=ml_process)
    processing_thread.start()


def capture_and_store_frames(rtsp_url, buffer_size=10):
    frame_storage = FrameStorage(buffer_size)
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
                # Store the frame in the buffer
                frame_storage.store_frame(buffer)

                if frame_storage.get_buffer_size() >= buffer_size:
                    print("Buffer full. Processing frames with ML model...")
                    # Process frames in a separate thread
                    async_ml_processing(frame_storage, process_frames_with_ml)

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


def main():
    load_dotenv("./configs/.env")
    rtsp_url = get_rtsp_url()
    logging.info(f"RTSP URL: {rtsp_url}")
    logging.info("Capturing frames and processing them with the ML service.")

    try:
        capture_and_store_frames(rtsp_url, buffer_size=30)
    except Exception as e:
        logging.error(f"An error occurred during the frame capture process: {e}")


if __name__ == "__main__":
    main()
