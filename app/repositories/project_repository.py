from typing import Protocol, Sequence
from app.models.project_model import Project
from app.utils import func

class ProjectRepository(Protocol):
    def get(self, project_code:int) -> Project | None: ...
    def create(self, title:str, description:str) -> Project: ...
    def update(self, project_code:int, title:str, description:str) -> Project: ...
    def filter(self, title:str|None=None) -> Sequence[Project]: ...
    def all(self) -> Sequence[Project]: ...
    def delete(self, project_code:int) -> None:...
    def count_all(self) -> int : ...


class InMemoryProjectRepository(ProjectRepository):

    def __init__(self) -> None:
        self.projects : list[Project] = list()

    def get(self, project_code:int) -> Project | None:
        for project in self.projects:
            if project.code == project_code:
                return project
        return None

    def create(self, title:str, description:str) -> Project:
        project_code = func.generate_random_id()
        if self.get(project_code=project_code):
            raise ValueError('project with this project_code already exists')
        if self.filter(title=title):
            raise ValueError('project with this title already exists')
        project = Project(code=project_code, title=title, description=description)
        self.projects.append(project)
        return project

    def update(self, project_code:int, title:str, description:str) -> Project:
        instance = self.get(project_code=project_code)
        if not instance:
            raise ValueError('project with this project_code does not exist')
        if self.filter(title=title):
            raise ValueError('project with this title already exists')
        instance.title = title
        instance.description = description
        return instance
    
    def filter(self, title: str | None = None) -> Sequence[Project]:
        result = list()
        for project in self.projects:
            if project.title == title:
                result.append(project)
        return result

    def all(self) -> Sequence[Project]:
        return self.projects

    def delete(self, project_code:int) -> None:
        from app.repositories.task_repository import in_memory_task_repo
        project = self.get(project_code=project_code)
        if not project:
            raise ValueError('project does not exist')
        self.projects.remove(project)
        tasks = in_memory_task_repo.filter(project_code=project_code)
        for task in tasks:
            in_memory_task_repo.delete(task_code=task.code)

    def count_all(self) -> int :
        return len(self.projects)


in_memory_project_repo = InMemoryProjectRepository()