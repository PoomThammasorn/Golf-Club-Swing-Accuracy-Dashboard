# ML/tests/test_main.py

from fastapi.testclient import TestClient
from main import app  # Use absolute import to access main.py

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "server is running"}
