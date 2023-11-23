from pydantic import BaseModel
from typing import Optional

class TaskResponse(BaseModel):
    id: Optional[int]
    name: str
    task: str


class TaskBody(BaseModel):
    name: str
    task: str