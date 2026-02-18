from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal, Annotated, Optional


class MovieBase(BaseModel):
    id: Optional[int] = None
    name: str
    price: int | float
    description: str
    imageUrl: Optional[str]
    location: Literal["SPB", "MSK"]
    published: bool
    genreId: Annotated[int, Field(ge=1, le=10)]
    rating: Optional[int | float] = None
    createdAt: Optional[datetime] = None
