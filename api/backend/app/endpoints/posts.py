from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import CursorResult

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.config import settings
from app.utils.token import get_current_active_user

from fastapi_cache.decorator import cache

import time

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/all", response_model=response_schemas.AllPosts)
@cache(expire=settings.CACHE_EXPIRE)
async def get_posts(
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get all posts
    """
    posts = crud.get_all_posts(db=db)

    time.sleep(3)

    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )

    return posts


@router.post("/create", response_model=None)
async def create_post(
    post: request_schemas.PostCreate,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a post
    """
    return crud.create_post(db=db, post=post, user_id=current_user.id)


@router.delete("/delete/{post_id}", response_model=response_schemas.Post)
async def delete_post(
    post_id: int,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a post
    """
    deleting_op = crud.delete_post(
        db=db,
        post_id=post_id,
        user_id=current_user.id,
    )

    if deleting_op is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No post for this user found",
        )


@router.put("/update", response_model=response_schemas.Post)
async def update_post(
    post: request_schemas.PostUpdate,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update a post
    """
    return crud.update_post(db=db, post=post)
