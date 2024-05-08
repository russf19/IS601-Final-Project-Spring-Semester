from builtins import ValueError, any, bool, str
from pydantic import BaseModel, EmailStr, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func
import uuid
import re
from app.models.user_model import UserRole
from app.utils.nickname_gen import generate_nickname

def validate_url(url: Optional[str]) -> Optional[str]:
    if url is None:
        return url
    url_regex = (
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:\S+(?::\S*)?@)?'  # user:pass authentication
        r'(?:[A-Za-z0-9.-]+|(?:\[[A-Fa-f0-9:\.]+\]))'  # IP or domain
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$'  # path
    )
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="joanna.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="Joanna")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/joanna.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/joannadoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/joannadoe")
    is_professional: Optional[bool] = Column(Boolean, default=False)
    role: UserRole

    _validate_urls = validator('profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True)(validate_url)
 
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    email: EmailStr = Field(..., example="joanna.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class UserUpdate(BaseModel):
    email: EmailStr = Field(..., example="joanna.doe1@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="Joanna")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Senior software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/joanna1.jpg")
    linkedin_profile_url: Optional[str] =Field(None, example="https://linkedin.com/in/joannadoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/joannadoe")
    is_professional: Optional[bool]
    updated_at: Optional[datetime]
    role: UserRole

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    email: EmailStr = Field(..., example="joanna.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())    
    is_professional: Optional[bool] = Field(default=False, example=False)
    professional_status_updated_at: Optional[datetime] = Field(None, example="2022-01-01T00:00:00Z")

    role: UserRole

class LoginRequest(BaseModel):
    email: str = Field(..., example="joanna.doe@example.com")
    password: str = Field(..., example="Secure*1234")

class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")

class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), "nickname": generate_nickname(), "email": "joanna.doe@example.com",
        "first_name": "Joanna", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "last_name": "Doe", "bio": "Experienced developer", "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/joanna.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/joannadoe", 
        "github_profile_url": "https://github.com/joannadoe"
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)
