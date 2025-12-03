import os
from dotenv import load_dotenv
from typing import Sequence
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.models.project_model import Project
from app.models.task_model import Task
from app.utils.func import generate_random_id
from app.utils.validators import validate_project_title, validate_project_description

load_dotenv()

class ProjectService:

    def __init__(self, project_repo:ProjectRepository, task_repo:TaskRepository) -> None:
        self.project_repo = project_repo
        self.task_repo = task_repo

    def create_project(self, title:str, description:str) -> Project:
        validate_project_title(title=title)
        validate_project_description(description=description)
        if self.project_repo.count_all() >= int(os.getenv('MAX_NUMBER_OF_PROJECT', 0)):
            raise ValueError('max number of project exceeded')
        return self.project_repo.create(title=title, description=description)
    
    def update_project(self, project_code:int, title:str, description:str) -> Project:
        validate_project_title(title=title)
        validate_project_description(description=description)
        return self.project_repo.update(project_code=project_code, title=title, description=description)

    def delete_project(self, project_code:int) -> None:
        self.project_repo.delete(project_code=project_code)

    def list_projects(self) -> Sequence[Project]:
        return self.project_repo.all()
    
    def list_project_tasks(self, project_code:int) -> Sequence[Task]:
        project = self.project_repo.get(project_code=project_code)
        if not project:
            raise ValueError('invalid project_code')
        return self.task_repo.filter(project_code=project_code)