from __future__ import annotations
from typing import Optional, List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    Table,
    DateTime,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)
    recipes_favori = relationship(
        "Recipe", secondary="user_recipe_favori", back_populates="users"
    )
    recipes_created: Mapped[List[Recipe]] = relationship(
        "Recipe", back_populates="users_has_created"
    )


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class IngredientRecipe(Base):
    __tablename__ = "ingredient_recipe"
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"), primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id"), primary_key=True
    )
    quantity: Mapped[float]
    unit: Mapped[Optional[str]]
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipes")


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String, unique=True)
    rating = Column(Float)
    total_time = Column(Integer)
    cook_time = Column(Integer)
    preparation_time = Column(Integer)
    pause_time = Column(Integer)
    difficulty = Column(String)
    cost = Column(String)
    nb_personne = Column(Integer)
    nb_commentary = Column(Integer)
    added_date = Column(DateTime, nullable=True)
    edit_date = Column(DateTime, nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"))

    users = relationship(
        "Users", secondary="user_recipe_favori", back_populates="recipes_favori"
    )
    users_has_created = relationship("Users", back_populates="recipes_created")
    user_id = Column(Integer, ForeignKey("users.id"))

    ingredients: Mapped[List["IngredientRecipe"]] = relationship(
        "IngredientRecipe", back_populates="recipe"
    )

    steps: Mapped[List["Step"]] = relationship(
        "Step",
        back_populates="recipe",
        order_by="Step.number",
        cascade="all, delete-orphan",
    )


class Ingredient(Base):
    __tablename__ = "ingredient"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String, unique=True)

    recipes: Mapped[List["IngredientRecipe"]] = relationship(
        "IngredientRecipe", back_populates="ingredient"
    )


class Rating(Base):
    __tablename__ = "recipe_rating"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))


class Step(Base):
    __tablename__ = "step"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    number = Column(Integer)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    recipe = relationship("Recipe", back_populates="steps")


user_recipe_favori = Table(
    "user_recipe_favori",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("recipe_id", ForeignKey("recipe.id")),
)
