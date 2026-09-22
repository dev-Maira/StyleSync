from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from app.db.session import get_db
from app.models.wardrobe import ClothingItem  # Apne clothing model class ka naam check kar lena
from app.core.config import settings

router = APIRouter(prefix="/agent", tags=["AI Agent"])

# Gemini Model Initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.7
)

@router.post("/suggest-outfit")
async def suggest_outfit(occasion: str, db: AsyncSession = Depends(get_db)):
    # 1. Fetch wardrobe items from DB
    result = await db.execute(select(ClothingItem))
    clothes = result.scalars().all()
    
    if not clothes:
        raise HTTPException(status_code=400, detail="Wardrobe is empty!")

    # 2. Format items for LLM
    inventory = "\n".join([f"- {item.name} ({item.category}, {item.color})" for item in clothes])

    # 3. LangChain Prompt Template
    prompt = PromptTemplate(
        input_variables=["occasion", "inventory"],
        template="""
        You are a professional fashion stylist AI.
        Based on the user's available wardrobe inventory below, suggest the best outfit for the occasion: '{occasion}'.

        Available Wardrobe:
        {inventory}

        Give a stylish recommendation and explain briefly why this combination works.
        """
    )

    # 4. LCEL Chain execution
    chain = prompt | llm
    response = chain.invoke({"occasion": occasion, "inventory": inventory})

    return {"occasion": occasion, "recommendation": response.content}