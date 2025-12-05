from fastapi import HTTPException, status
from app.api.v1.schemas.request import ErrorSchema


class APIException(HTTPException):

    def __init__(self, status:int=status.HTTP_400_BAD_REQUEST, code:int=0, message:str|None=None,  *args, **kwargs):
        self.status = status
        self.code = code
        self.message = message
        error = ErrorSchema(code=code, message=message)
        super().__init__(status_code=status, detail=error.model_dump(), *args, **kwargs)

