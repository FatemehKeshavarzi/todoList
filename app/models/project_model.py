from app.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .task_model import Task

class Project(BaseModel):
    __tablename__ = 'project'

    code : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(30), unique=True)
    description : Mapped[str] = mapped_column(String(150))
    tasks : Mapped[list['Task']] = relationship(back_populates='project', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return str(self.code)
