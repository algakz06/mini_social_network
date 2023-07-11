from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict


class UserInDB(BaseModel):
    """
    User in database schema
    """
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    hashed_password: str
