from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.wardrobe import ClothingItem
from app.models.users import User  # Fixed import name
from app.schemas.wardrobe import ClothingItemCreate, ClothingResponse  # Fixed response schema name
from app.api.deps import get_current_user

router = APIRouter(prefix="/clothing", tags=["Clothing"])


@router.post("/", response_model=ClothingResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    clothing_data: ClothingItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = ClothingItem(
        name=clothing_data.name,
        category=clothing_data.category,
        color=clothing_data.color,
        season=clothing_data.season,
        brand=clothing_data.brand,
        user_id=current_user.id
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item


@router.get("/", response_model=List[ClothingResponse])
async def get_items(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ClothingItem).where(ClothingItem.user_id == current_user.id)
    )
    return result.scalars().all()


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ClothingItem).where(ClothingItem.id == item_id, ClothingItem.user_id == current_user.id)
    )
    item = result.scalars().first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Clothing item not found"
        )

    await db.delete(item)
    await db.commit()
    return None