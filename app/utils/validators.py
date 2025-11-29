from datetime import date

def validate_deadline(deadline:date) -> bool:
    if deadline >= date.today():
        return True
    return False


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