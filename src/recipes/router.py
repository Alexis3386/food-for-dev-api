from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from models import Recipe, Users, IngredientRecipe, Ingredient, Step
from .schemas import (
    RecipeRequest,
    IngredientRecipeSch,
    StepSch,
    RecipeDetail,
    AddIngredientToRecipe,
    RecipeBase,
)
from database import SessionLocal
from auth.router import get_current_user
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime
from sqlalchemy import select

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/category/{category_id}", status_code=status.HTTP_200_OK)
async def get_recipe_by_category(
    db: db_dependency, category_id: int
) -> Page[RecipeBase]:
    return paginate(
        db,
        db.query(Recipe).filter(Recipe.category_id == category_id).order_by(Recipe.id),
    )
    # if recipe_list is None:
    #     raise HTTPException(status_code=401, detail='')
    # return recipe_list


@router.get("/ingredients/{recipe_id}", status_code=status.HTTP_200_OK)
async def get_ingredients_recipe(
    db: db_dependency, recipe_id: int
) -> list[IngredientRecipeSch]:
    ingredients = (
        db.query(IngredientRecipe.quantity, IngredientRecipe.unit, Ingredient.name)
        .filter(Recipe.id == IngredientRecipe.recipe_id)
        .filter(Recipe.id == recipe_id)
        .filter(IngredientRecipe.ingredient_id == Ingredient.id)
        .all()
    )
    return ingredients


@router.get("/steps/{recipe_id}", status_code=status.HTTP_200_OK)
async def get_steps_recipe(db: db_dependency, recipe_id: int) -> list[StepSch]:
    return db.query(Step).filter(Step.recipe_id == recipe_id).all()


@router.get("/{recipe_id}", status_code=status.HTTP_200_OK)
async def get_recipe_by_id(db: db_dependency, recipe_id: int) -> Optional[RecipeDetail]:
    # Sélection des colonnes spécifiques pour Recipe
    recipe_query = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    # Sélection des colonnes spécifiques pour IngredientRecipe et Ingredient
    ingredients_query = (
        db.query(
            IngredientRecipe.quantity,
            IngredientRecipe.unit,
            Ingredient.name,
            Ingredient.id,
        )
        .join(Ingredient, IngredientRecipe.ingredient_id == Ingredient.id)
        .filter(IngredientRecipe.recipe_id == recipe_id)
        .all()
    )

    # Sélection des colonnes spécifiques pour Step
    steps_query = (
        db.query(Step.number, Step.description)
        .filter(Step.recipe_id == recipe_id)
        .order_by(Step.number)
        .all()
    )

    if not recipe_query:
        return None
    # Reconstruction du résultat sous forme de dictionnaire ou d'objet
    recipe_details = {
        **recipe_query.__dict__,
        "ingredients": [
            {"quantity": ing.quantity, "unit": ing.unit, "name": ing.name, "id": ing.id}
            for ing in ingredients_query
        ],
        "steps": [
            {"number": step.number, "description": step.description}
            for step in steps_query
        ],
    }

    return RecipeDetail(**recipe_details)


@router.post("/favorite_recipe/{recipe_id}", status_code=status.HTTP_200_OK)
async def add_user_recipe_favori(
    db: db_dependency, user: user_dependency, recipe_id: int
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user is None or recipe is None:
        raise HTTPException(status_code=404, detail="User or Recipe not found")
    user_model.recipes_favori.append(recipe)
    db.commit()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_recipe(
    db: db_dependency, user: user_dependency, create_recipe_request: RecipeRequest
):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User or Recipe not found")
    create_recipe_model = Recipe(
        name=create_recipe_request.name,
        rating=create_recipe_request.rating,
        total_time=create_recipe_request.total_time,
        cook_time=create_recipe_request.cook_time,
        preparation_time=create_recipe_request.preparation_time,
        pause_time=create_recipe_request.pause_time,
        difficulty=create_recipe_request.difficulty,
        cost=create_recipe_request.cost,
        nb_personne=create_recipe_request.nb_personne,
        category_id=create_recipe_request.category_id,
        added_date=datetime.now(),
        nb_commentary=0,
    )
    db.add(create_recipe_model)
    user_model.recipes_created.append(create_recipe_model)
    db.commit()


@router.post(
    "/add_ingredient/{recipe_id}/{ingredient_id}", status_code=status.HTTP_201_CREATED
)
async def create_recipe(
    db: db_dependency,
    user: user_dependency,
    add_ingredient_request: AddIngredientToRecipe,
):
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User or Recipe not found")
    create_ingredient_recipe_model = IngredientRecipe(
        recipe_id=add_ingredient_request.recipe_id,
        ingredient_id=add_ingredient_request.ingredient_id,
        quantity=add_ingredient_request.quantity,
        unit=add_ingredient_request.unit,
    )
    db.add(create_ingredient_recipe_model)
    db.commit()


@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK)
async def delete_recipe(db: db_dependency, user: user_dependency, recipe_id: int):
    if user.get("user_role") == "admin" or get_recipe_user_id(
        db, recipe_id
    ) == user.get("id"):
        db.query(Step).filter(Step.recipe_id == recipe_id).delete()
        db.query(IngredientRecipe).filter(
            IngredientRecipe.recipe_id == recipe_id
        ).delete()
        db.query(Recipe).filter(Recipe.id == recipe_id).delete()
        db.commit()
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")


@router.patch("/{recipe_id}", status_code=status.HTTP_200_OK)
async def update_recipe(
    db: db_dependency,
    user: user_dependency,
    recipe_id: int,
    update_recipe_request: RecipeRequest,
):
    if user.get("user_role") == "admin" or get_recipe_user_id(
        db, recipe_id
    ) == user.get("id"):
        stored_recipe_data = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not stored_recipe_data:
            raise HTTPException(status_code=404, detail="Recipe not found")

        # Mettre à jour seulement les champs fournis dans la requête
        update_data = update_recipe_request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(stored_recipe_data, key, value)

            # Mettre à jour le champ edit_date
            stored_recipe_data.edit_date = datetime.now()

            db.add(stored_recipe_data)
            db.commit()
            db.refresh(
                stored_recipe_data
            )  # Rafraîchit l'instance pour obtenir les données actuelles

            return stored_recipe_data

    raise HTTPException(status_code=401, detail="Authentication failed")


def get_recipe_user_id(db: db_dependency, recipe_id: int) -> None | int:
    stmt = select(Recipe.user_id).where(Recipe.id == recipe_id)
    return db.execute(stmt).first()[0]
