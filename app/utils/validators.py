from datetime import date
from app.models import TaskStatus

def validate_task_deadline(deadline:date) -> None:
    if deadline < date.today():
        raise ValueError('invalid date')


def validate_project_title(title:str) -> None:
    if len(title) > 30:
        raise ValueError('title must be less than 30 characters')


def validate_project_description(description:str):
    if len(description) > 150:
            raise ValueError('description must be less that 150 characters')


def validate_task_title(title:str) -> None:
    if len(title) > 30:
        raise ValueError('title must be less than 30 characters')


def validate_task_description(description:str):
    if len(description) > 150:
        raise ValueError('description must be less that 150 characters')


def validate_task_status(status:TaskStatus):
    if not status in ['done', 'todo', 'doing']:
        raise ValueError('status must be one of done | todo | doing')
