from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CategoryEnum(str, Enum):
    TOP = "Top"
    BOTTOM = "Bottom"
    SHOES = "Shoes"
    OUTERWEAR = "Outerwear"
    ACCESSORY = "Accessory"


class SeasonEnum(str, Enum):
    SUMMER = "Summer"
    WINTER = "Winter"
    SPRING = "Spring"
    FALL = "Fall"
    ALL_SEASON = "All Season"


class ClothingItemCreate(BaseModel):
    name: str
    category: CategoryEnum
    color: str
    season: SeasonEnum
    brand: str


class ClothingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    category: str
    color: str
    season: str
    brand: str
    created_at: datetime

    class Config:
        from_attributes = True


class OutfitCreate(BaseModel):
    name: str
    occasion: str
    item_ids: List[int]


class OutfitResponse(BaseModel):
    id: int
    user_id: int
    name: str
    occasion: str
    created_at: datetime
    items: List[ClothingResponse]

    class Config:
        from_attributes = True