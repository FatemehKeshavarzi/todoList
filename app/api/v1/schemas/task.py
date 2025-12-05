from datetime import datetime, date
from pydantic import BaseModel, Field
from app.models import TaskStatus


class BaseTaskSchema(BaseModel):
    title: str = Field(max_length=30)
    description: str = Field(max_length=150)
    status: TaskStatus = TaskStatus.TODO
    deadline: date | None = None


class TaskCreateRequestSchema(BaseTaskSchema):
    pass


class TaskCreateResponseSchema(BaseTaskSchema):
    code: int
    created_time: datetime
    

class TaskUpdateRequestSchema(BaseTaskSchema):
    pass
    

class TaskUpdateResponseSchema(TaskCreateResponseSchema):
    pass


class TaskListSchema(TaskCreateResponseSchema):
    pass