import os
from dotenv import load_dotenv
from app.repositories.project_repository import in_memory_project_repo, ProjectRepository
from app.repositories.task_repository import in_memory_task_repo, TaskRepository
from app.models.project_model import Project
from app.utils.func import generate_random_id

load_dotenv()

class ProjectService:

    def __init__(self, repo:ProjectRepository) -> None:
        self.repo = repo

    def create_project(self, title:str, description:str) -> Project:
        if len(self.repo.all()) >= int(os.getenv('MAX_NUMBER_OF_PROJECT', 0)):
            raise ValueError('max number of project exceeded')
        if len(title) > 30:
            raise ValueError('title must be less than 30 characters')
        if len(description) > 150:
            raise ValueError('description must be less that 150 characters')
        project = Project(project_id=generate_random_id(), title=title, description=description)
        self.repo.create(project=project)
        return project
        