from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(BaseModel):
    title: str
    file_type: str

class DocumentCreate(DocumentBase):
    content: str

class Document(DocumentBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Query schemas
class QueryBase(BaseModel):
    question: str

class QueryCreate(QueryBase):
    pass

class Query(QueryBase):
    id: int
    answer: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Action schemas
class ActionBase(BaseModel):
    action_type: str
    details: str

class ActionCreate(ActionBase):
    pass

class Action(ActionBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 