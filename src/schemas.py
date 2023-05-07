from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class SearchQuery(BaseModel):
    query: str

class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True

class SearchQuery(BaseModel):
    query: str

class ContactBirthday(BaseModel):
    id: int
    full_name: str
    birthday: date
    days_until_birthday: Optional[int]