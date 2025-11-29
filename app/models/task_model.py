from dataclasses import dataclass
from typing import Literal


@dataclass
class Task:
    task_id : int
    project_id : int
    title : str
    description : str
    deadline: str | None = None
    status : Literal['done', 'doing', 'todo'] = 'todo'