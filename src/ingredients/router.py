from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from auth.router import get_current_user
from database import SessionLocal
from models import Ingredient, IngredientRecipe, Users
from .schemas import IngredientRequest

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/find_by_name/{name}", status_code=status.HTTP_200_OK)
def get_ingredient_exist(db: db_dependency, name: str) -> bool:
    match = db.query(Ingredient).filter(Ingredient.name == name).count()
    return match >= 1


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_ingredient_by_id(db: db_dependency, id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == id).first()
    return ingredient


@router.get("/user/favorite_ingredient", status_code=status.HTTP_200_OK)
async def get_user_ingredient_favorite(db: db_dependency, user: user_dependency):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    return user_model.ingredients_favori


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_ingredient(
        db: db_dependency,
        create_ingredient_request: IngredientRequest,
        user: user_dependency,
) -> None:
    create_ingredient_model = Ingredient(name=create_ingredient_request.name)
    db.add(create_ingredient_model)
    db.commit()


@router.put("/{ingredient_id}", status_code=status.HTTP_200_OK)
def update_ingredient(
        db: db_dependency,
        user: user_dependency,
        ingredient_id: int,
        update_ingredient_request: IngredientRequest
):
    stored_ingredient_data = (
        db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    )
    if stored_ingredient_data is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    stored_ingredient_data.name = update_ingredient_request.name
    db.add(stored_ingredient_data)
    db.commit()


@router.delete("/{ingredient_id}", status_code=status.HTTP_200_OK)
def delete_ingredient(db: db_dependency, user: user_dependency, ingredient_id: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredients_query = (
        db.query(IngredientRecipe)
        .filter(IngredientRecipe.ingredient_id == ingredient_id)
        .all()
    )
    if len(ingredients_query) > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ingredient use in some recipe",
        )

    db.delete(ingredient)
    db.commit()


@router.post("/favorite_ingredient/{ingredient_id}", status_code=status.HTTP_200_OK)
async def add_user_ingredient_favori(
        db: db_dependency, user: user_dependency, ingredient_id: int
):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user is None or ingredient is None:
        raise HTTPException(status_code=404, detail="User or Ingredient not found")
    user_model.ingredients_favori.append(ingredient)
    db.commit()
