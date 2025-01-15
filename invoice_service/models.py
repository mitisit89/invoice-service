from datetime import datetime

from sqlmodel import Field, SQLModel


class Application(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_name: str = Field(index=True)
    description: str
    created_at: datetime = Field(default=datetime.now())
