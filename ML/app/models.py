from pydantic import BaseModel


class ResultData(BaseModel):
    angle: float
    distance: float


class ResultPayload(BaseModel):
    task_id: int
    data: ResultData
