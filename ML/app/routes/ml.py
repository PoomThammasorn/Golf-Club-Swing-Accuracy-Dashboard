from fastapi import APIRouter
from app.models import ResultPayload, ResultData
from app.config import settings
import requests

router = APIRouter()


@router.post("/ml/data/{task_id}")
async def process_data(task_id: int):
    print(f"Processing data for task ID: {task_id}")

    # URL to send result back to NodeJS
    node_webhook_url = f"{settings.NODE_WEBHOOK_URL}/ml/result"
    payload = ResultPayload(task_id=task_id, data=ResultData(angle=0.5, distance=0.2))

    try:
        # Send the result back to the NodeJS service
        response = requests.post(node_webhook_url, json=payload.model_dump_json())

        if response.status_code == 200:
            return {"status": "Success"}
        else:
            return {"status": "Failed to send result", "code": response.status_code}

    except requests.exceptions.RequestException as e:
        return {"status": "Failed to send result", "error": str(e)}
