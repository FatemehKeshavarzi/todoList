from dataclasses import dataclass
from typing import Literal


@dataclass
class Task:
    project_id : int
    title : str
    description : str
    status : Literal['done', 'doing', 'todo'] = 'todo'