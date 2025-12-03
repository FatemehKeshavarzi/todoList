from typing import Protocol, Sequence
from datetime import date
from app.models import Task, TaskStatus
from app.utils import func


class TaskRepository(Protocol):
    def get(self, task_code:int) -> Task | None: ...
    def create(self, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task: ...
    def update(self, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task: ...
    def filter(self, project_code:int|None=None) -> Sequence[Task]: ...
    def all(self) -> Sequence[Task]: ...
    def delete(self, task_code:int) -> None:...
    def count_all(self) -> int : ...

class InMemoryTaskRepository(TaskRepository):

    def __init__(self) -> None:
        self.tasks : list[Task] = list()

    def get(self, task_code: int) -> Task | None:
        for task in self.tasks:
            if task.code == task_code:
                return task
        return None
    
    def create(self, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        from app.repositories.project_repository import in_memory_project_repo
        task_code = func.generate_random_id()
        project = in_memory_project_repo.get(project_code=project_code)
        if not project:
            raise ValueError('invalid project_code')
        if self.get(task_code=task_code):
            raise ValueError('task with this task_code already exists')
        task = Task(code=task_code, project_code=project_code, title=title, description=description, deadline=deadline, status=status)
        self.tasks.append(task)
        return task
    
    def update(self, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        instance = self.get(task_code=task_code)
        if not instance:
            raise ValueError('task with this task_code does not exist')
        instance.status = status
        instance.deadline = deadline
        instance.title = title
        instance.description = description
        return instance
    
    def filter(self, project_code: int | None = None) -> Sequence[Task]:
        result = list()
        for task in self.tasks:
            if task.project_code == project_code:
                result.append(task)
        return result
    
    def all(self) -> Sequence[Task]:
        return self.tasks
    
    def delete(self, task_code: int) -> None:
        task = self.get(task_code=task_code)
        if not task:
            raise ValueError('task does not exist')
        self.tasks.remove(task)

    def count_all(self) -> int :
        return len(self.tasks)
    


in_memory_task_repo = InMemoryTaskRepository()
