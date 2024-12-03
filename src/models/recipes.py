# Standard Library
from typing import List, Optional

# Dependencies
from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str


class Recipe(BaseModel):
    id: Optional[str] = Field(None, description="generated recipe uuid v4")
    name: str
    description: str
    ingredients: List[Ingredient]
