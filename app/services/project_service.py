from app.repositories.project_repository import in_memory_project_repo, ProjectRepository
from app.repositories.task_repository import in_memory_task_repo, TaskRepository

class ProjectService:

    def __init__(self, repo:ProjectRepository) -> None:
        self.repo = repo

    def create_project()