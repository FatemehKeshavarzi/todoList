from typing import Literal, TypeVar
from pydantic import BaseModel

data_type = TypeVar('data_type')

class ResponseSchema[data_type](BaseModel):
    is_ok: bool = True
    data: data_type
    code: int


class ErrorSchema(BaseModel):
    is_ok: bool = False
    code: int
    message: str | None = None