from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict

Tag = Literal["food", "culture", "nature"]


class WishlistCreate(BaseModel):
    city: str = Field(min_length=1, max_length=80)
    poi_id: str = Field(min_length=1, max_length=140)
    name: str = Field(min_length=1, max_length=240)
    address: Optional[str] = Field(default=None, max_length=400)
    tag: Tag


class WishlistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: str
    poi_id: str
    name: str
    address: Optional[str]
    tag: Tag
