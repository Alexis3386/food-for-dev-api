from typing import Optional

from pydantic import BaseModel, Field


class IngredientRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3)
