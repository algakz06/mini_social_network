from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from typing import Union

from app.models import db_models, models
from app.schemas import response_schemas, request_schemas
from app.config import log
from app.utils.token import get_password_hash


def get_user(
    db: Session, email: Union[str, None]
) -> Union[models.UserInDB, None]:
    try:
        return models.UserInDB.model_validate(
            db.query(
                db_models.User.username.label('username'),
                db_models.User.email.label('email'),
                db_models.User.hashed_password.label('hashed_password'),
            )
            .filter(
                db_models.User.email == email,
            )
            .one()
        )
    except NoResultFound:
        return None


def create_user(db: Session, user: request_schemas.UserCreate) -> response_schemas.User:
    db_user = db_models.User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user = response_schemas.User.model_validate(db_user)

    log.info(f"Created user: {db_user}")
    return db_user
