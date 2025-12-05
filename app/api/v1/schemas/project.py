from datetime import datetime
from pydantic import BaseModel, Field


class BaseProjectSchema(BaseModel):
    title : str = Field(max_length=30)
    description : str = Field(max_length=150)


class ProjectCreateRequestSchema(BaseProjectSchema):
    pass


class ProjectCreateResponseSchema(BaseProjectSchema):
    code : int
    created_time : datetime


class ProjectUpdateRequestSchema(BaseProjectSchema):
    pass


class ProjectUpdateResponseSchema(ProjectCreateResponseSchema):
    pass


class ProjectListSchema(ProjectCreateResponseSchema):
    pass