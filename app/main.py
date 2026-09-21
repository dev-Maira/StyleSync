from fastapi import FastAPI
from app.api import auth, clothing, outfits
from app.db.session import engine
from app.models.base import Base  # File path apne project ke mutabiq adjust karein

app = FastAPI(
    title="StyleSync API",
    description="Asynchronous RESTful API for Wardrobe & Outfit Management",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(clothing.router, prefix="/clothing", tags=["Wardrobe"])
app.include_router(outfits.router, prefix="/outfits", tags=["Outfits"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)