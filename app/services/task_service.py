import os
from dotenv import load_dotenv
from datetime import date
from app.repositories.task_repository import TaskRepository
from app.models import Task, TaskStatus
from app.utils.func import generate_random_id
from app.utils.validators import validate_task_title, validate_task_description, validate_task_deadline, validate_task_status

load_dotenv()

class TaskService:

    def __init__(self, task_repo:TaskRepository) -> None:
        self.task_repo = task_repo

    def create_task(self, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=title)
        validate_task_status(status=status)
        if deadline:
            validate_task_deadline(deadline=deadline)
        if self.task_repo.count_all() >= int(os.getenv('MAX_NUMBER_OF_TASK', 0)):
            raise ValueError('max number of task exceeded')
        return self.task_repo.create(project_code=project_code, title=title, description=description, deadline=deadline, status=status)
    
    def update_task(self, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=description)
        validate_task_status(status=status)
        if deadline:
            validate_task_deadline(deadline=deadline)
        return self.task_repo.update(task_code=task_code, title=title, description=description, deadline=deadline, status=status)
    
    def delete_task(self, task_code:int) -> None:
        self.task_repo.delete(task_code=task_code)
