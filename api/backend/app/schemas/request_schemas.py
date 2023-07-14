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


class PostUpdate(BaseModel):
    """
    Post update schema
    """

    id: int
    title: str
    content: str

    model_config = {
        "json_schema_extra": {
            "example": {"id": 1, "title": "title", "content": "loremipsum"}
        }
    }


class PostCreate(BaseModel):
    """
    Post create schema
    """

    user_id: int
    title: str
    content: str

    model_config = {
        "json_schema_extra": {
            "example": {"user_id": 1, "title": "title", "content": "content"}
        }
    }


class ReactionCreate(BaseModel):
    """
    Reaction create schema
    """

    post_id: int
    user_id: int
    reaction_type: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"post_id": 1, "user_id": 1, "reaction_type": "like"},
                {"post_id": 1, "user_id": 1, "reaction_type": "dislike"},
            ]
        }
    }
