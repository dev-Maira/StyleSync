from sqlalchemy import Table, Column, ForeignKey, DateTime, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

# Junction Table
outfit_items = Table(
    "outfit_items",
    Base.metadata,
    Column("outfit_id", ForeignKey("outfits.id", ondelete="CASCADE"), primary_key=True),
    Column("clothing_item_id", ForeignKey("clothingitem.id", ondelete="CASCADE"), primary_key=True),
)

class ClothingItem(Base):
    __tablename__ = "clothingitem"  # Aapka exact original name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=False)
    season: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Outfit(Base):
    __tablename__ = "outfits"  # Aapka exact original name

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    occasion: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    items: Mapped[list["ClothingItem"]] = relationship(secondary=outfit_items)