from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    user_name: str = Field(..., title="User Name", min_length=1, max_length=100)
    description: str = Field(..., title="Description", min_length=1, max_length=1000)


class ApplicationResponse(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes: bool = True
