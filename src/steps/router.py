from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from auth.router import get_current_user
from database import SessionLocal
from models import Step
from .schemas import StepRequest

router = APIRouter(prefix="/steps", tags=["steps"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_step(
    db: db_dependency,
    create_step_request: StepRequest,
    user: user_dependency,
) -> None:
    create_ingredient_model = Step(
        number=create_step_request.number,
        description=create_step_request.description,
        recipe_id=create_step_request.recipe_id,
    )
    db.add(create_ingredient_model)
    db.commit()


@router.put("/{step_id}", status_code=status.HTTP_200_OK)
def update_step(
    db: db_dependency,
    user: user_dependency,
    step_id: int,
    update_step_request: StepRequest,
):
    stored_step_data = db.query(Step).filter(Step.id == step_id).first()
    if stored_step_data is None:
        raise HTTPException(status_code=404, detail="Step not found")
    stored_step_data.description = update_step_request.description
    stored_step_data.number = update_step_request.number
    db.add(stored_step_data)
    db.commit()


@router.delete("/{step_id}", status_code=status.HTTP_200_OK)
def delete_step(db: db_dependency, user: user_dependency, step_id: int):
    step = db.query(Step).filter(Step.id == step_id).first()
    if step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    db.delete(step)
    db.commit()
