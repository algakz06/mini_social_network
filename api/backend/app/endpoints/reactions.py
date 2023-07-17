from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.config import settings
from app.utils.token import get_current_active_user

router = APIRouter(
    prefix="/reactions",
    tags=["reactions"],
)


@router.post("/add", response_model=None)
async def add_reaction(
    reaction: request_schemas.ReactionCreate,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Add a reaction
    """
    post_author_id = crud.get_post_author_id(db=db, post_id=reaction.post_id)

    if post_author_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found",
        )

    if post_author_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot react to your own post",
        )

    adding_reaction_result = crud.add_reaction(
        db=db, reaction=reaction, user_id=current_user.id
    )

    if reaction is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reaction already exists",
        )

    return adding_reaction_result


@router.delete("/delete", response_model=None)
async def delete_reaction(
    reaction: request_schemas.ReactionDelete,
    current_user: response_schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete a reactions
    """
    deleting_op = crud.delete_reaction(
        db=db, reaction=reaction, user_id=current_user.id
    )

    if deleting_op is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reaction not found",
        )

    return deleting_op
