from dataclasses import dataclass


@dataclass
class Project:
    project_id : int
    title : str
    description: str
