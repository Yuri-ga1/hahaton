from fastapi import APIRouter, HTTPException
import asyncio
from .schemas import *
from database_module.database import database
   
router = APIRouter()

@router.post("/addEvent")
async def create_event(event: Event):
    # дата начала и дата конца
    await database.add_event(event.name, event.description)
    

@router.post("/addCards")
async def create_card(card: Card):
    rarity_id = await database.get_rarity_id(card.rarity)
    if rarity_id:
        is_exist = await database.get_card(card.name)
        if is_exist is None:
            await database.add_card(
                name=card.name,
                type=card.type,
                rarity_id=rarity_id,
                hp=card.hp,
                damage=card.damage,
                speed=card.speed
            )
        else:
            raise HTTPException(409, detail=f"Card {card.name} alredy exists")
    else:
        raise HTTPException(422, detail="Invalid rarity name")