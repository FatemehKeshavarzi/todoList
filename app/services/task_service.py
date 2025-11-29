import os
from dotenv import load_dotenv
from app.repositories.project_repository import in_memory_project_repo, ProjectRepository
from app.repositories.task_repository import in_memory_task_repo, TaskRepository
from app.models.project_model import Project
from app.models.task_model import Task
from app.utils.func import generate_random_id
from app.utils.validators import validate_task_title, validate_task_description

load_dotenv()

class TaskService:

    def __init__(self, repo:TaskRepository) -> None:
        self.repo = repo

    def create_task(self, project_id:int, title:str, description:str, deadline:str|None=None, status:str='todo'):
        validate_task_title(title=title)
        validate_task_description(description=title)
        if len(self.repo.all()) >= int(os.getenv('MAX_NUMBER_OF_TASK', 0)):
            raise ValueError('max number of task exceeded')
        task = Task(task_id=generate_random_id(), project_id=project_id, title=title, description=description, deadline=deadline, status=status)
        return self.repo.create(task=task)
    
    