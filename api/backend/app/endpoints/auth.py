from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from typing import Annotated
from datetime import timedelta

from app.config import log
from app.schemas import response_schemas, request_schemas
from app.core.dependencies import get_db
from app.core import crud
from app.config import settings
from app.utils.token import (
    authenticate_user,
    create_access_token,
)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create", response_model=response_schemas.User)
async def create_user(
    user: request_schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user
    """
    db_user = crud.get_user(db, user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return crud.create_user(db=db, user=user)


@router.post("/token", response_model=response_schemas.Token)
async def login_for_access_token(
    user_data: request_schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
