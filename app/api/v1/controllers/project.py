from fastapi import APIRouter, HTTPException, status
from app.services.project_service import ProjectService
from app.api.v1.schemas.request import ResponseSchema, ErrorSchema
from app.api.v1.schemas.project import ProjectCreateRequestSchema, ProjectCreateResponseSchema, ProjectListSchema, ProjectUpdateRequestSchema, ProjectUpdateResponseSchema
from app.repositories.project_repository import SQLProjectRepository, InMemoryProjectRepository
from app.repositories.task_repository import SQLTaskRepository, InMemoryTaskRepository
from app.exceptions.api_exceptions import APIException

router = APIRouter()


@router.get('/projects', response_model=ResponseSchema[list[ProjectListSchema]], responses={400: {"model": ErrorSchema}})
def list_projects():
    try:
        project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
        projects = project_service.list_projects()
        return ResponseSchema(code=1, data=projects)
    except Exception as e:
        raise APIException(message=str(e))


@router.post('/projects', response_model=ResponseSchema[ProjectCreateResponseSchema], responses={400: {"model": ErrorSchema}})
def add_project(data: ProjectCreateRequestSchema):
    try:
        project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
        project = project_service.create_project(title=data.title, description=data.description)
        return ResponseSchema(code=1, data=project)
    except Exception as e:
        raise APIException(message=str(e))


@router.put('/projects/{project_code}', response_model=ResponseSchema[ProjectUpdateResponseSchema], responses={400: {"model": ErrorSchema}})
def update_project(project_code:int, data:ProjectUpdateRequestSchema):
    try:
        project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
        project = project_service.update_project(project_code=project_code, title=data.title, description=data.description)
        return ResponseSchema(code=1, data=project)
    except Exception as e:
        raise APIException(message=str(e))


@router.delete('/projects/{project_code}', response_model=ResponseSchema[str], responses={400: {"model": ErrorSchema}})
def delete_project(project_code:int):
    try:
        project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
        project_service.delete_project(project_code=project_code)
        return ResponseSchema(code=1, data='deleted')
    except Exception as e:
        raise APIException(message=str(e))
