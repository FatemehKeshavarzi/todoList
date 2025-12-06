import os
from dotenv import load_dotenv
from datetime import date, datetime
from app.repositories.task_repository import TaskRepository
from app.models import Task, TaskStatus
from app.utils.validators import validate_task_title, validate_task_description, validate_task_deadline, validate_task_status
from app.db.session import SessionLocal
load_dotenv()

class TaskService:

    def __init__(self, task_repo:TaskRepository) -> None:
        self.task_repo = task_repo

    def create_task(self, project_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=title)
        validate_task_status(status=status)
        if deadline:
            validate_task_deadline(deadline=deadline)
        with SessionLocal.begin() as session:
            if self.task_repo.count_all(session=session) >= int(os.getenv('MAX_NUMBER_OF_TASK', 0)):
                raise ValueError('max number of task exceeded')
            return self.task_repo.create(session=session, project_code=project_code, title=title, description=description, deadline=deadline, status=status)
    
    def update_task(self, task_code:int, title:str, description:str, deadline:date|None, status:TaskStatus) -> Task:
        validate_task_title(title=title)
        validate_task_description(description=description)
        validate_task_status(status=status)
        if deadline:
            validate_task_deadline(deadline=deadline)
        with SessionLocal.begin() as session:
            task = self.task_repo.get(session=session, task_code=task_code)
            if not task:
                raise ValueError('task not found')
            closed_at = datetime.now() if status == TaskStatus.DONE else task.closed_at
            return self.task_repo.update(session=session, task_code=task_code, title=title, description=description, deadline=deadline, status=status, closed_at=closed_at)
    
    def delete_task(self, task_code:int) -> None:
        with SessionLocal.begin() as session:
            self.task_repo.delete(session=session, task_code=task_code)

    def update_epired_tasks(self) -> None:
        with SessionLocal.begin() as session:
            expired_tasks = self.task_repo.filter(session=session, status__in=[TaskStatus.DOING, TaskStatus.TODO], deadline__lt=date.today())
            for task in expired_tasks:
                self.task_repo.update(session=session, task_code=task.code, title=task.title, description=task.description, deadline=task.deadline, status=TaskStatus.DONE, closed_at=datetime.now())