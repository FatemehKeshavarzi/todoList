import os
from dotenv import load_dotenv
from typing import Literal, Sequence
from datetime import date
from app.repositories.task_repository import TaskRepository
from app.models.project_model import Project
from app.models.task_model import Task
from app.utils.func import generate_random_id
from app.utils.validators import validate_task_title, validate_task_description, validate_task_deadline
from app.utils.func import parse_deadline

load_dotenv()

class TaskService:

    def __init__(self, repo:TaskRepository) -> None:
        self.repo = repo

    def create_task(self, project_id:int, title:str, description:str, deadline:str|None, status:Literal['done', 'doing', 'todo']) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=title)
        if len(self.repo.all()) >= int(os.getenv('MAX_NUMBER_OF_TASK', 0)):
            raise ValueError('max number of task exceeded')
        task = Task(task_id=generate_random_id(), project_id=project_id, title=title, description=description, deadline=deadline, status=status)
        return self.repo.create(task=task)
    
    def update_task(self, task_id:int, title:str, description:str, deadline:str|None, status:Literal['done', 'doing', 'todo']) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=description)
        if deadline:
            deadline_date : date = parse_deadline(deadline=deadline)
            validate_task_deadline(deadline=deadline_date)
        return self.repo.update(task_id=task_id, title=title, description=description, deadline=deadline, status=status)
    
    def delete_task(self, task_id:int) -> None:
        self.repo.delete(task_id=task_id)

    def list_tasks(self, project_id) -> Sequence[Task]:
        return self.repo.filter(project_id=project_id)