from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from app.db.base import Base

class BaseModel(Base):
    __abstract__ =  True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_time : Mapped[datetime] = mapped_column(DateTime, default=datetime.now)