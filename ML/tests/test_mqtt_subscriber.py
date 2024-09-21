import os
import base64
import numpy as np
import cv2
import pytest
from unittest.mock import patch, MagicMock
from mqtt_subscriber import setup_mqtt_client, on_message


@pytest.fixture
def mock_mqtt_client():
    with patch('paho.mqtt.client.Client') as MockClient:
        yield MockClient


@pytest.fixture(autouse=True)
def load_env_vars(monkeypatch):
    monkeypatch.setenv("MQTT_URL", "mqtt://test_broker")
    monkeypatch.setenv("MQTT_TOPIC", "test/topic")


@patch('paho.mqtt.client.Client')
@patch('mqtt_subscriber.load_dotenv')
def test_setup_mqtt_client(self, mock_load_dotenv, MockClient):
    # Arrange
    mock_client = MockClient.return_value
    # Ensure this is set to the correct URL
    os.environ["MQTT_URL"] = "localhost"
    os.environ["MQTT_TOPIC"] = "camera/data"

    # Act
    setup_mqtt_client()

    # Assert
    mock_client.connect.assert_called_once_with("localhost")
    mock_client.subscribe.assert_called_once_with("camera/data")
    mock_client.loop_start.assert_called_once()


def test_on_message_decodes_image():
    global last_frame
    last_frame = None

    # Create a dummy image and encode it as base64
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)  # Black image
    _, encoded_image = cv2.imencode('.jpg', dummy_image)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')

    message_mock = MagicMock()
    message_mock.payload = base64_image.encode('utf-8')

    # Act
    on_message(None, None, message_mock)

    # Assert
    assert last_frame is not None, "last_frame should not be None after decoding the image"
    assert last_frame.shape == (
        100, 100, 3), "last_frame shape does not match the expected shape"
    assert (last_frame == dummy_image).all(
    ), "Decoded image does not match the original dummy image"


if __name__ == '__main__':
    pytest.main()
