import os
from datetime import date
from dotenv import load_dotenv
from typing import Protocol, Any, Iterable
from app.models.task_model import Task

load_dotenv()

class TaskRepository(Protocol):
    def get(self, task_id:int) -> Task | None: ...
    def create(self, task:Task) -> Task: ...
    def update(self, task:Task) -> Task: ...
    def filter(self, project_id:int|None=None) -> Iterable[Task]: ...
    def all(self) -> Iterable[Task]: ...
    def delete(self, task_id:int) -> None:...

class InMemoryTaskRepository(TaskRepository):

    def __init__(self) -> None:
        self.tasks : list[Task] = list()

    def get(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def create(self, task:Task) -> Task:
        if len(self.tasks) >= int(os.getenv('MAX_NUMBER_OF_TASK', 0)):
            raise ValueError('max number of task exceeded')
        from app.repositories.project_repository import in_memory_project_repo
        if not in_memory_project_repo.get(project_id=task.project_id):
            raise ValueError('invalid project_id')
        instance = self.get(task_id=task.task_id)
        if instance:
            raise ValueError('task with this task_id already exists')
        if task.status not in ['done', 'doing', 'todo']:
            raise ValueError('invalid status')
        self.tasks.append(task)
        return task
    
    def update(self, task: Task) -> Task:
        instance = self.get(task_id=task.task_id)
        if not instance:
            raise ValueError('task with this task_id does not exist')
        if task.status not in ['done', 'doing', 'todo']:
            raise ValueError('invalid status')
        instance.status = task.status
        instance.deadline = task.deadline
        instance.title = task.title
        instance.description = task.description
        return instance
    
    def filter(self, project_id: int | None = None) -> Iterable[Task]:
        result = list()
        for task in self.tasks:
            if task.project_id == project_id:
                result.append(task)
        return result
    
    def all(self) -> Iterable[Task]:
        return self.tasks
    
    def delete(self, task_id: int) -> None:
        task = self.get(task_id=task_id)
        if not task:
            raise ValueError('task does not exist')
        self.tasks.remove(task)


in_memory_task_repo = InMemoryTaskRepository()
