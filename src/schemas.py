from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ContactModel(BaseModel):

    id: int
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: str = Field(max_length=30)
    phone: str = Field(max_length=15)
    birthday: datetime
    additional_info: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class UpdateContact(BaseModel):

    name: Optional[str] = Field(None, max_length=15)
    surname: Optional[str] = Field(None, max_length=15)
    email: Optional[str] = Field(None, max_length=30)
    phone: Optional[str] = Field(None, max_length=15)
    birthday: Optional[datetime] = None
    additional_info: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
