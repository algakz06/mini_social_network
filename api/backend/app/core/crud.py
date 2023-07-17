from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from typing import Union

from app.models import db_models, models
from app.schemas import response_schemas, request_schemas
from app.config import log
from app.utils.token import get_password_hash


def get_user(db: Session, email: Union[str, None]) -> Union[models.UserInDB, None]:
    try:
        return models.UserInDB.model_validate(
            db.query(
                db_models.Users.id.label("id"),
                db_models.Users.username.label("username"),
                db_models.Users.email.label("email"),
                db_models.Users.hashed_password.label("hashed_password"),
            )
            .filter(
                db_models.Users.email == email,
            )
            .one()
        )
    except NoResultFound:
        return None


def get_post_author_id(db: Session, post_id: int) -> Union[int, None]:
    try:
        return (
            db.query(db_models.Posts.user_id)
            .filter(db_models.Posts.id == post_id)
            .one()[0]
        )
    except NoResultFound:
        return None


def create_user(db: Session, user: request_schemas.UserCreate) -> response_schemas.User:
    db_user = db_models.Users(
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


def create_post(
    db: Session, post: request_schemas.PostCreate, user_id: int
) -> response_schemas.Post:
    db_post = db_models.Posts(
        title=post.title,
        content=post.content,
        user_id=user_id,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    db_post = response_schemas.Post.model_validate(db_post)

    log.info(f"Created post {db_post}")
    return db_post


def delete_post(
    db: Session, post_id: int, user_id: int
) -> Union[response_schemas.Post, None]:
    try:
        db_post = (
            db.query(db_models.Posts)
            .filter(
                db_models.Posts.id == post_id,
                db_models.Posts.user_id == user_id
            )
            .one()
        )
        db.delete(db_post)
        db.commit()

        db_post = response_schemas.Post.model_validate(db_post)

        log.info(f"Deleted post {db_post}")
        return db_post
    except NoResultFound:
        return None


def chech_is_post_exists(db: Session, post_id: int) -> bool:
    try:
        db.query(db_models.Posts).filter(db_models.Posts.id == post_id).one()
        return True
    except NoResultFound:
        return False


def update_post(
    db: Session, post: request_schemas.PostUpdate
) -> Union[response_schemas.Post, None]:
    db_post = db.query(db_models.Posts).filter(db_models.Posts.id == post.id).first()

    if db_post is None:
        return None

    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)

    db_post = response_schemas.Post.model_validate(db_post)

    log.info(f"Edited post {db_post}")

    return db_post


def add_reaction(
    db: Session, reaction: request_schemas.ReactionCreate, user_id: int
) -> Union[response_schemas.Reaction, None]:
    if reaction.reaction_type == "like":
        reaction_type = db_models.ReactionType.LIKE
    elif reaction.reaction_type == "dislike":
        reaction_type = db_models.ReactionType.DISLIKE
    else:
        return None

    try:
        db_reaction = db_models.Reactions(
            post_id=reaction.post_id,
            user_id=user_id,
            reaction_type=reaction_type,
        )
        db.add(db_reaction)
        db.commit()
        db.refresh(db_reaction)
    except NoResultFound:
        return None

    db_reaction = response_schemas.Reaction.model_validate(db_reaction)

    log.info(f"Added reaction {db_reaction}")

    return db_reaction


def get_all_posts(db: Session) -> Union[response_schemas.AllPosts, None]:
    try:
        return response_schemas.AllPosts(
            count=db.query(db_models.Posts).count(),
            posts=[
                response_schemas.Post.model_validate(post)
                for post in db.query(
                    db_models.Posts.id.label("id"),
                    db_models.Posts.user_id.label("user_id"),
                    db_models.Posts.title.label("title"),
                    db_models.Posts.content.label("content"),
                ).all()
            ],
        )
    except NoResultFound:
        return None


def delete_reaction(
    db: Session, reaction: request_schemas.ReactionDelete, user_id: int
) -> Union[response_schemas.Reaction, None]:
    try:
        db_reaction = (
            db.query(db_models.Reactions)
            .filter(
                db_models.Reactions.post_id == reaction.post_id,
                db_models.Reactions.user_id == user_id,
            )
            .one()
        )
        db.delete(db_reaction)
        db.commit()
    except NoResultFound:
        return None

    db_reaction = response_schemas.Reaction.model_validate(db_reaction)

    log.info(f"Deleted reaction {db_reaction}")

    return db_reaction
