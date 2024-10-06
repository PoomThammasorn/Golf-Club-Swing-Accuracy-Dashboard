import time
import logging
from collections import deque


class FrameStorage:
    def __init__(self, buffer_size=10):
        self.buffer_size = buffer_size
        self.frame_buffer = deque(maxlen=buffer_size)

    def store_frame(self, frame_data):
        data = {"data": frame_data, "timestamp": time.time()}
        self.frame_buffer.append(data)
        logging.info(f"Stored frame. Current buffer size: {len(self.frame_buffer)}")

    def clear_buffer(self):
        self.frame_buffer.clear()
        logging.info("Cleared frame buffer.")

    def get_buffered_frames(self):
        buffered_frames = list(self.frame_buffer)  # Convert deque to a list
        self.clear_buffer()
        logging.info(
            f"Returning {len(buffered_frames)} buffered frames and clearing buffer."
        )
        return buffered_frames

    def get_frame_by_timestamp(self, timestamp, tolerance=1):
        frame_to_return = None
        for frame in self.frame_buffer:
            if abs(frame["timestamp"] - timestamp) <= tolerance:
                frame_to_return = frame
                break
        self.clear_buffer()
        return frame_to_return

    def get_buffer_size(self):
        return len(self.frame_buffer)
