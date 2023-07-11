from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator


class UserCreate(BaseModel):
    """
    User create schema
    """
    email: EmailStr
    password: str
    username: str


class UserLogin(BaseModel):
    """
    User login schema
    """
    email: EmailStr
    password: str
