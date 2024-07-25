from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from auth.router import get_current_user
from database import SessionLocal
from models import Category
from .schemas import CategoryRequest

router = APIRouter(prefix="/category", tags=["category"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
def get_category(db: db_dependency) -> list[tuple[Any]]:
    """
    Retrieve all categories from the database.

    Parameters:
        - db: Dependency injection for the database session.

    Returns:
        - A list of CategoryRequest objects representing all categories.
    """
    category = db.query(Category).all()
    return category


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    db: db_dependency,
    user: user_dependency,
    category_request: CategoryRequest,
):
    """
    Creates a new category in the database.

    Args:
        db (Session): The database session.
        user (dict): The current user.
        category_request (CategoryRequest): The request data for creating the category.

    Returns:
        None
    """
    create_category_model = Category(name=category_request.name)
    db.add(create_category_model)
    db.commit()


@router.put("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(
    db: db_dependency,
    user: user_dependency,
    category_id: int,
    update_category_request: CategoryRequest,
):
    """
    Updates a category in the database with the given ID.

    Args:
        db (Session): The database session.
        user (dict): The current user.
        category_id (int): The ID of the category to update.
        update_category_request (CategoryRequest): The request data for updating the category.

    Returns:
        Category: The updated category object.

    Raises:
        HTTPException: If the category with the given ID is not found.
    """
    stored_category_data = db.query(Category).filter(Category.id == category_id).first()
    if stored_category_data is None:
        raise HTTPException(status_code=404, detail="Category not found")
    stored_category_data.name = update_category_request.name
    db.add(stored_category_data)
    db.commit()
    return stored_category_data
