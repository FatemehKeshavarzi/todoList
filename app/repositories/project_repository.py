from typing import Protocol, Sequence
from app.models.project_model import Project


class ProjectRepository(Protocol):
    def get(self, project_id:int) -> Project | None: ...
    def create(self, project:Project) -> Project: ...
    def update(self, project_id:int, title:str, description:str) -> Project: ...
    def filter(self, title:str|None=None) -> Sequence[Project]: ...
    def all(self) -> Sequence[Project]: ...
    def delete(self, project_id:int) -> None:...
    def count_all(self) -> int : ...


class InMemoryProjectRepository(ProjectRepository):

    def __init__(self) -> None:
        self.projects : list[Project] = list()

    def get(self, project_id:int) -> Project | None:
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    def create(self, project:Project) -> Project:
        instance = self.get(project_id=project.project_id)
        if instance:
            raise ValueError('project with this project_id already exists')
        instance = self.filter(title=project.title)
        if instance:
            raise ValueError('project with this title already exists')
        self.projects.append(project)
        return project

    def update(self, project_id:int, title:str, description:str) -> Project:
        instance = self.get(project_id=project_id)
        if not instance:
            raise ValueError('project with this project_id does not exist')
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

    def delete(self, project_id:int) -> None:
        from app.repositories.task_repository import in_memory_task_repo
        project = self.get(project_id=project_id)
        if not project:
            raise ValueError('project does not exist')
        self.projects.remove(project)
        tasks = in_memory_task_repo.filter(project_id=project_id)
        for task in tasks:
            in_memory_task_repo.delete(task_id=task.task_id)

    def count_all(self) -> int :
        return len(self.projects)


in_memory_project_repo = InMemoryProjectRepository()