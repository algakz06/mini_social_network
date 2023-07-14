from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from app.models.db_models import ReactionType


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    disabled: bool | None = None


class Post(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    title: str
    content: str
    user_id: int


class Reaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    post_id: int
    user_id: int
    reaction_type: ReactionType


class AllPosts(BaseModel):
    count: int
    posts: List[Post]
