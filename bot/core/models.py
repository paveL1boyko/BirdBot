from pydantic import BaseModel, Field


class SessionData(BaseModel):
    user_agent: str = Field(validation_alias="User-Agent")
    proxy: str | None = None


from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    id: str = Field(..., alias="_id")  # Переименование поля _id
    title: str
    logo: str
    channelId: Optional[str] = ""
    slug: str
    is_enable: bool
    priority: int
    point: int
    url: Optional[str] = ""
    v: int = Field(..., alias="__v")  # Переименование поля __v
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")



class JoinedTask(BaseModel):
    id: str = Field(..., alias="_id")
    taskId: str
    telegramId: str
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")
    v: int = Field(..., alias="__v")
