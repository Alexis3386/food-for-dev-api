from typing import Optional

from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3)
