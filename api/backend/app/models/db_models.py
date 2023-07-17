from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())


class ReactionType(enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class Reactions(Base):
    __tablename__ = "reactions"
    id = Column(Integer, primary_key=True)
    reaction_type = Column(Enum(ReactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, default=datetime.now())

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_reaction"),
    )
