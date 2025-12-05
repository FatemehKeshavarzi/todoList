from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.controllers import project as v1_project
from app.api.v1.controllers import task as v1_task
from app.exceptions.api_exceptions import APIException
from app.api.v1.schemas.request import ErrorSchema

app = FastAPI()

app.include_router(v1_project.router, prefix="/api/v1", tags=["v1"])
app.include_router(v1_task.router, prefix="/api/v1", tags=["v1"])

@app.exception_handler(APIException)
async def v1_api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status,
        content=ErrorSchema(code=exc.code, message=exc.message).model_dump()
    )



