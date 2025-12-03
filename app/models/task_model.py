from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date, Enum
from enum import StrEnum
from app.models.base import BaseModel

if TYPE_CHECKING:
    from .project_model import Project


class TaskStatus(StrEnum):
    DONE = 'done'
    DOING = 'doing'
    TODO = 'todo'


class Task(BaseModel):
    __tablename__ = 'task' 

    code : Mapped[int] = mapped_column(unique=True)
    project_id : Mapped[int] = mapped_column(ForeignKey('project.id'))
    title : Mapped[str] = mapped_column(String(30))
    description : Mapped[str] = mapped_column(String(150))
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    status : Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.TODO)
    project : Mapped['Project'] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        return str(self.code)