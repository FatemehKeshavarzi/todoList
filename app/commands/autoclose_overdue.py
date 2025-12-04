from typing import Literal
from app.services.task_service import TaskService
from app.repositories.task_repository import SQLTaskRepository, InMemoryTaskRepository
from config import STORAGE

def update_expired_tasks(storage: Literal['memory', 'sql'] = STORAGE):
    if storage == 'memory':
        task_repository = InMemoryTaskRepository()
    elif storage == 'sql':
        task_repository = SQLTaskRepository()
    else:
        raise ValueError('invalid storage type. [memory | sql]')
    TaskService(task_repo=task_repository)
    print('update_expired_tasks DONE')