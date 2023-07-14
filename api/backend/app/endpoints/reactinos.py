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
    return crud.add_reaction(db=db, reaction=reaction)
