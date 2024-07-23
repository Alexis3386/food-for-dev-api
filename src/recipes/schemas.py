from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class RecipeBase(BaseModel):
    id: int
    name: str
    rating: float
    total_time: int
    cook_time: int
    preparation_time: int
    pause_time: int
    difficulty: str
    cost: str
    nb_personne: int
    nb_commentary: int
    category_id: int

    class Config:
        from_attributes = True


class RecipeRequest(BaseModel):
    name: Optional[str] = None
    total_time: Optional[int] = None
    rating: float = Field(default=0.0)
    cook_time: Optional[int] = None
    preparation_time: Optional[int] = None
    pause_time: int = Field(default=0)
    cost: Optional[str] = None
    difficulty: Optional[str] = None
    nb_personne: Optional[int] = None
    category_id: Optional[int] = None
    added_date: datetime = Field(default=datetime.fromtimestamp(0))
    edit_date: datetime = Field(default=datetime.fromtimestamp(0))


class IngredientRecipeSch(BaseModel):
    quantity: float
    unit: Optional[str] = None
    name: str
    id: int


class StepSch(BaseModel):
    number: int
    description: str


class RecipeDetail(RecipeBase):
    steps: List[StepSch]
    ingredients: List[IngredientRecipeSch]


class AddIngredientToRecipe(BaseModel):
    recipe_id: int
    ingredient_id: int
    quantity: Optional[float] = None
    unit: Optional[str] = None
