import os
from dotenv import load_dotenv
from typing import Sequence
from app.repositories.project_repository import ProjectRepository
from app.models.project_model import Project
from app.utils.func import generate_random_id
from app.utils.validators import validate_project_title, validate_project_description

load_dotenv()

class ProjectService:

    def __init__(self, repo:ProjectRepository) -> None:
        self.repo = repo

    def create_project(self, title:str, description:str) -> Project:
        validate_project_title(title=title)
        validate_project_description(description=description)
        if len(self.repo.all()) >= int(os.getenv('MAX_NUMBER_OF_PROJECT', 0)):
            raise ValueError('max number of project exceeded')
        project = Project(project_id=generate_random_id(), title=title, description=description)
        return self.repo.create(project=project)
    
    def update_project(self, project_id:int, title:str, description:str) -> Project:
        validate_project_title(title=title)
        validate_project_description(description=description)
        return self.repo.update(project_id=project_id, title=title, description=description)

    def delete_project(self, project_id:int) -> None:
        self.repo.delete(project_id=project_id)

    def list_projects(self) -> Sequence[Project]:
        return self.repo.all()