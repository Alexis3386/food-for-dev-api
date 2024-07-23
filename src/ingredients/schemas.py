from pydantic import BaseModel, Field
from typing import Optional


class IngredientRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3)
