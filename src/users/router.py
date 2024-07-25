from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status

from auth.router import get_current_user, bcrypt_context
from database import SessionLocal
from models import Users
from .schemas import UserVerification

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    user_model = db.scalar(select(Users).where(Users.id == user.get("id")))
    if user_model is None:
        raise HTTPException(status_code=401, detail="")
    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
        user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(
            user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")

    hashed_password = bcrypt_context.hash(user_verification.new_password)
    user_model.hashed_password = hashed_password
    db.add(user_model)
    db.commit()
