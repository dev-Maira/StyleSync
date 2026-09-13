from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db
from app.models.wardrobe import ClothingItem, Outfit  # <-- Updated to Outfit
from app.models.users import User
from app.schemas.wardrobe import OutfitCreate, OutfitResponse, ClothingResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/outfits", tags=["Outfits"])


@router.post("/", response_model=OutfitResponse, status_code=status.HTTP_201_CREATED)
async def create_outfit(
    outfit_data: OutfitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check for duplicate outfit name for this user
    existing_outfit = await db.execute(
        select(Outfit).where(
            Outfit.user_id == current_user.id,
            Outfit.name.ilike(outfit_data.name)
        )
    )
    if existing_outfit.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An outfit named '{outfit_data.name}' already exists in your wardrobe."
        )

    # Fetch valid items owned by user
    result = await db.execute(
        select(ClothingItem).where(
            ClothingItem.id.in_(outfit_data.item_ids),
            ClothingItem.user_id == current_user.id
        )
    )
    items = result.scalars().all()

    if len(items) != len(set(outfit_data.item_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more item IDs are invalid or do not belong to you."
        )

    new_outfit = Outfit(
        name=outfit_data.name,
        occasion=outfit_data.occasion,
        user_id=current_user.id,
        items=items
    )

    db.add(new_outfit)
    await db.commit()

    stmt = (
        select(Outfit)
        .options(selectinload(Outfit.items))
        .where(Outfit.id == new_outfit.id)
    )
    refreshed_result = await db.execute(stmt)

    return refreshed_result.scalars().first()

@router.get("/", response_model=List[OutfitResponse])
async def get_user_outfits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = (
        select(Outfit)  # <-- Updated model reference
        .options(selectinload(Outfit.items))
        .where(Outfit.user_id == current_user.id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/recommend", response_model=List[ClothingResponse])
async def recommend_outfit(
    season: str,
    occasion: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stmt = select(ClothingItem).where(
        ClothingItem.user_id == current_user.id,
        ClothingItem.season.ilike(season)
    )
    result = await db.execute(stmt)
    items = result.scalars().all()

    tops = [item for item in items if item.category.lower() in ["top", "shirt", "t-shirt"]]
    bottoms = [item for item in items if item.category.lower() in ["bottom", "pants", "jeans", "skirt"]]
    shoes = [item for item in items if item.category.lower() in ["shoes", "footwear"]]

    if not tops or not bottoms or not shoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not enough items to assemble an outfit for season '{season}'."
        )

    return [tops[0], bottoms[0], shoes[0]]