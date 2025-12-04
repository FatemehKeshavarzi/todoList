from typing import Protocol, Sequence
from sqlalchemy import select, func as sa_func
from sqlalchemy.orm import Session
from app.models import Project
from app.utils import func


class ProjectRepository(Protocol):
    def get(self, session:Session, project_code:int) -> Project | None: ...
    def create(self, session:Session, title:str, description:str) -> Project: ...
    def update(self, session:Session, project_code:int, title:str, description:str) -> Project: ...
    def filter(self, session:Session, title:str|None=None) -> Sequence[Project]: ...
    def all(self, session:Session) -> Sequence[Project]: ...
    def delete(self, session:Session, project_code:int) -> None:...
    def count_all(self, session:Session) -> int : ...


class InMemoryProjectRepository(ProjectRepository):
    """
    Singleton pattern for one-time initialization
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.projects : list[Project] = list()

    def get(self, session:Session, project_code:int) -> Project | None:
        for project in self.projects:
            if project.code == project_code:
                return project
        return None

    def create(self, session:Session, title:str, description:str) -> Project:
        project_code = func.generate_random_id()
        if self.get(session=session, project_code=project_code):
            raise ValueError('project with this project_code already exists')
        if self.filter(session=session, title=title):
            raise ValueError('project with this title already exists')
        project = Project(code=project_code, title=title, description=description)
        self.projects.append(project)
        return project

    def update(self, session:Session, project_code:int, title:str, description:str) -> Project:
        instance = self.get(session=session, project_code=project_code)
        if not instance:
            raise ValueError('project with this project_code does not exist')
        if any(p for p in self.filter(session=session, title=title) if p.code != project_code):
            raise ValueError("project with this title already exists")
        instance.title = title
        instance.description = description
        return instance
    
    def filter(self, session:Session, title: str | None = None) -> Sequence[Project]:
        result = list()
        for project in self.projects:
            if project.title == title:
                result.append(project)
        return result

    def all(self, session:Session) -> Sequence[Project]:
        return self.projects

    def delete(self, session:Session, project_code:int) -> None:
        from app.repositories.task_repository import InMemoryTaskRepository
        project = self.get(session=session, project_code=project_code)
        if not project:
            raise ValueError('project does not exist')
        self.projects.remove(project)
        in_memory_task_repo = InMemoryTaskRepository()
        tasks = in_memory_task_repo.filter(session=session, project_code=project_code)
        for task in tasks:
            in_memory_task_repo.delete(session=session, task_code=task.code)

    def count_all(self, session:Session) -> int :
        return len(self.projects)



class SQLProjectRepository(ProjectRepository):


    def get(self, session:Session, project_code: int) -> Project | None:
        stmt = select(Project).where(Project.code == project_code)
        return session.scalar(stmt)

    def create(self, session:Session, title: str, description: str) -> Project:
        project = Project(title=title, description=description)
        session.add(project)
        return project

    def update(self, session:Session, project_code: int, title: str, description: str) -> Project:
        project = self.get(session=session, project_code=project_code)
        if not project:
            raise ValueError("project not found")

        project.title = title
        project.description = description
        return project

    def filter(self, session:Session, title: str | None = None):
        stmt = select(Project)
        if title:
            stmt = stmt.where(Project.title == title)
        return session.scalars(stmt).all()

    def all(self, session:Session):
        stmt = select(Project)
        return session.scalars(stmt).all()

    def delete(self, session:Session, project_code: int) -> None:
        project = self.get(session=session, project_code=project_code)
        if not project:
            raise ValueError("project not found")
        session.delete(project)

    def count_all(self, session:Session) -> int:
        stmt = select(sa_func.count(Project.code))
        return session.scalar(stmt) or 0
