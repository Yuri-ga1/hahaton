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
    
    
@router.post('/addRarity')
async def add_rarity(new_rarity: Rarity):
    old_rarity = await database.get_rarity_id(new_rarity.name)
    if old_rarity:
        raise HTTPException(409, detail=f"Rarity {new_rarity.name} alredy exists")
    else:
        await database.add_rarity(new_rarity.name, new_rarity.chance)
        

@router.post('/addType')
async def add_type(new_type: Type):
    old_type = await database.get_type_id(new_type.name)
    if old_type:
        raise HTTPException(409, detail=f"Type {new_type.name} alredy exists")
    else:
        await database.add_type(new_type.name, new_type.dominate)