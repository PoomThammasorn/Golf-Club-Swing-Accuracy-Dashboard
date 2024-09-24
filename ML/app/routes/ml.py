from fastapi import APIRouter, BackgroundTasks
from app.models import ResultPayload, ResultData
from app.config import settings
import httpx  # Use httpx for async requests
import asyncio  # Import asyncio for async sleep

router = APIRouter()


async def process_ml_data(task_id: int):
    # Simulate processing time of 5 seconds (non-blocking)
    await asyncio.sleep(5)

    # Create a result payload after processing
    result_payload = ResultPayload(
        task_id=task_id, data=ResultData(angle=0.5, distance=0.2)
    )

    # URL to send result back to NodeJS
    node_webhook_url = f"{settings.NODE_WEBHOOK_URL}/api/ml/result"

    print(f"Sending processed result to {node_webhook_url} with task_id: {task_id}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                node_webhook_url, json=result_payload.model_dump()
            )

        if response.status_code != 200:
            print(
                f"Failed to send result for task_id: {task_id}, status code: {response.status_code}"
            )

    except httpx.RequestError as e:
        print(f"Error sending result for task_id: {task_id}, error: {str(e)}")


@router.post("/ml/data/{task_id}")
async def process_data(task_id: int, background_tasks: BackgroundTasks):
    print(f"Received data request for task_id: {task_id}")

    # Add the ML processing task to the background
    background_tasks.add_task(process_ml_data, task_id)

    # Acknowledge the receipt of data immediately
    return {
        "status": "Success",
        "message": f"Data processing started for task_id: {task_id}",
    }
