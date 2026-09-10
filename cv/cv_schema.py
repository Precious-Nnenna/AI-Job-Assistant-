from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CVCreate(BaseModel):
    filename: str
    content: str


class CVOut(BaseModel):
    filename: str
    content: str
    uploaded_at: datetime

    class Config:
        from_attributes = True