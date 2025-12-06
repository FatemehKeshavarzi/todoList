from fastapi import APIRouter
from app.api.v1.schemas.request import ResponseSchema, ErrorSchema
from app.api.v1.schemas.task import TaskCreateRequestSchema, TaskCreateResponseSchema, TaskUpdateRequestSchema, TaskUpdateResponseSchema, TaskListSchema
from app.repositories.task_repository import SQLTaskRepository, InMemoryTaskRepository
from app.repositories.project_repository import SQLProjectRepository, InMemoryProjectRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.exceptions.api_exceptions import APIException


router = APIRouter()


@router.get('/projects/{project_code}/tasks', response_model=ResponseSchema[list[TaskListSchema]], responses={400:{'model':ErrorSchema}})
def list_tasks(project_code:int):
    try:
        project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
        tasks = project_service.list_project_tasks(project_code=project_code)
        return ResponseSchema(code=1, data=tasks)

    except Exception as e:
        raise APIException(message=str(e))


@router.post('/projects/{project_code}', response_model=ResponseSchema[TaskCreateResponseSchema], responses={400:{'model':ErrorSchema}})
def add_task(project_code:int, data:TaskCreateRequestSchema):
    try:
        task_service = TaskService(task_repo=SQLTaskRepository())
        task = task_service.create_task(project_code=project_code, title=data.title, description=data.description, deadline=data.deadline, status=data.status)
        return ResponseSchema(code=1, data=task)

    except Exception as e:
        raise APIException(message=str(e))


@router.put('/projects/tasks/{task_code}', response_model=ResponseSchema[TaskUpdateResponseSchema], responses={400:{'model':ErrorSchema}})
def update_task(task_code:int, data:TaskUpdateRequestSchema):
    try:
        task_service = TaskService(task_repo=SQLTaskRepository())
        task = task_service.update_task(task_code=task_code, title=data.title, description=data.description, deadline=data.deadline, status=data.status)
        return ResponseSchema(code=1, data=task)

    except Exception as e:
        raise APIException(message=str(e))


@router.delete('/projects/tasks/{task_code}', response_model=ResponseSchema[str], responses={400:{'model':ErrorSchema}})
def delete_task(task_code:int):
    try:
        task_service = TaskService(task_repo=SQLTaskRepository())
        task_service.delete_task(task_code=task_code)
        return ResponseSchema(code=1, data='deleted')

    except Exception as e:
        raise APIException(message=str(e))
    