from typing import Protocol, Sequence
from datetime import date
from sqlalchemy import select, func as sa_func
from sqlalchemy.orm import Session
from app.models import Task, TaskStatus, Project
from app.models import Task, TaskStatus
from app.utils import func


class TaskRepository(Protocol):
    def get(self, session:Session, task_code:int) -> Task | None: ...
    def create(self, session:Session, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task: ...
    def update(self, session:Session, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task: ...
    def filter(self, session:Session, project_code: int | None = None, status: TaskStatus | None = None) -> Sequence[Task]: ...
    def all(self, session:Session) -> Sequence[Task]: ...
    def delete(self, session:Session, task_code:int) -> None:...
    def count_all(self, session:Session) -> int : ...

class InMemoryTaskRepository(TaskRepository):

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
            self.tasks : list[Task] = list()

    def get(self, session:Session, task_code: int) -> Task | None:
        for task in self.tasks:
            if task.code == task_code:
                return task
        return None
    
    def create(self, session:Session, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        from app.repositories.project_repository import InMemoryProjectRepository
        task_code = func.generate_random_id()
        in_memory_project_repo = InMemoryProjectRepository()
        project = in_memory_project_repo.get(session=session, project_code=project_code)
        if not project:
            raise ValueError('invalid project_code')
        if self.get(session=session, task_code=task_code):
            raise ValueError('task with this task_code already exists')
        task = Task(code=task_code, project_code=project_code, title=title, description=description, deadline=deadline, status=status)
        self.tasks.append(task)
        return task
    
    def update(self, session:Session, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        instance = self.get(session=session, task_code=task_code)
        if not instance:
            raise ValueError('task with this task_code does not exist')
        instance.status = status
        instance.deadline = deadline
        instance.title = title
        instance.description = description
        return instance
    
    def filter(self, session:Session, project_code: int | None = None, status: TaskStatus | None = None) -> Sequence[Task]:
        result = list()
        for task in self.tasks:
            if project_code is not None and task.project_code != project_code:
                continue
            if status is not None and task.status != status:
                continue
            result.append(task)
        return result
    
    def all(self, session:Session) -> Sequence[Task]:
        return self.tasks
    
    def delete(self, session:Session, task_code: int) -> None:
        task = self.get(session=session, task_code=task_code)
        if not task:
            raise ValueError('task does not exist')
        self.tasks.remove(task)

    def count_all(self, session:Session) -> int :
        return len(self.tasks)
    


class SQLTaskRepository(TaskRepository):

    def get(self, session:Session, task_code: int) -> Task | None:
        stmt = select(Task).where(Task.code == task_code)
        return session.scalar(stmt)

    def create(
        self,
        session:Session,
        project_code: int,
        title: str,
        description: str,
        deadline: date | None,
        status: TaskStatus,
    ) -> Task:
        stmt_project = select(Project).where(Project.code == project_code)
        project = session.scalar(stmt_project)
        if not project:
            raise ValueError("invalid project_code")

        task = Task(
            project_code=project_code,
            title=title,
            description=description,
            deadline=deadline,
            status=status,
        )

        session.add(task)
        return task

    def update(
        self,
        session:Session,
        task_code: int,
        title: str,
        description: str,
        deadline: date | None,
        status: TaskStatus,
    ) -> Task:
        task = self.get(session=session, task_code=task_code)
        if not task:
            raise ValueError("task with this task_code does not exist")

        task.title = title
        task.description = description
        task.deadline = deadline
        task.status = status

        return task

    def filter(self, session:Session, project_code: int | None = None, status: TaskStatus | None = None) -> Sequence[Task]:
        conditions = []
        if project_code is not None:
            conditions.append(Task.project_code == project_code)
        if status is not None:
            conditions.append(Task.status == status)
        stmt = select(Task).where(*conditions)
        return session.scalars(stmt).all()

    def all(self, session:Session) -> Sequence[Task]:
        stmt = select(Task)
        return session.scalars(stmt).all()

    def delete(self, session:Session, task_code: int) -> None:
        task = self.get(session=session, task_code=task_code)
        if not task:
            raise ValueError("task does not exist")

        session.delete(task)

    def count_all(self, session:Session) -> int:
        stmt = select(sa_func.count(Task.code))
        return session.scalar(stmt) or 0
