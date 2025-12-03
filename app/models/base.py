from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from app.db.base import Base

class BaseModel(Base):
    __abstract__ =  True

    created_time : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __init__(self, **kw: Any):
        super().__init__(**kw)
        if self.created_time == None:
            self.created_time = datetime.now()