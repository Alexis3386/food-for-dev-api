from pydantic import BaseModel, Field


class StepRequest(BaseModel):
    description: str = Field(min_length=3)
    number: int = Field(gt=0)
    recipe_id: int
