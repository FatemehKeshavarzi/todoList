from typing import Protocol, Any, Iterable
from app.models.project_model import Project

class ProjectRepository(Protocol):
    def get(self, key:str, value:Any) -> Project | None: ...
    def create(self, project:Project) -> Project: ...
    def update(self, project:Project) -> Project: ...
    def all(self) -> Iterable[Project]: ...
    def delete(self, project_id:int) -> None:...


class InMemoryProjectRepository(ProjectRepository):

    def __init__(self) -> None:
        self.projects : list[Project] = list()

    def get(self, key:str, value:Any) -> Project | None:
        for project in self.projects:
            if getattr(project, key) == value:
                return project
        return None

    def create(self, project:Project) -> Project:
        instance = self.get(key='project_id', value=project.project_id)
        if instance:
            raise ValueError('project with this project_id already exists')
        instance = self.get(key='title', value=project.title)
        if instance:
            raise ValueError('project with this title already exists')
        self.projects.append(project)
        return project

    def update(self, project:Project) -> Project:
        if self.get(key='title', value=project.title):
            raise ValueError('project with this title already exists')
        instance = self.get(key='project_id', value=project.project_id)
        if not instance:
            raise ValueError('project with this project_id does not exist')
        instance.title = project.title
        instance.description = project.description
        return instance
    
    def all(self) -> Iterable[Project]:
        return self.projects

    def delete(self, project_id:int) -> None:
        project = self.get(key='project_id', value=project_id)
        if not project:
            raise ValueError('project does not exist')
        self.projects.remove(project)
    