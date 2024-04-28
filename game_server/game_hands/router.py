from fastapi import APIRouter, HTTPException
import asyncio
from .schemas import *
from database_module.database import database
   
router = APIRouter()

@router.post("/addEvent")
async def create_event(event: Event):
    if event.start < event.end:
        await database.add_event(event.name, event.description, event.start, event.end)
    else:
        raise HTTPException(409, detail=f"Еhe start date cannot be later than the end date")
    

@router.post("/addCards")
async def create_card(card: Card):
    rarity_id = await database.get_rarity_id(card.rarity)
    if rarity_id:
        is_exist = await database.get_card(card.name)
        if is_exist is None:
            type_id = await database.get_type_id(card.type)
            if type_id:
                await database.add_card(
                    name=card.name,
                    type_id=type_id,
                    rarity_id=rarity_id,
                    hp=card.hp,
                    damage=card.damage,
                    speed=card.speed
                )
            else:
                raise HTTPException(409, detail=f"Type {card.type} is not exists")
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
        
@router.post("/addCardToEvent")
async def add_card_to_event(card_event: CardToEvent):
    card = await database.get_card(card_event.card_name)
    event = await database.get_event(card_event.event_name)
    
    if card is None:
        raise HTTPException(404, "Card is not exist")
    if event is None:
        raise HTTPException(404, "Event is not exist")
    
    await database.add_card_to_event(card.id, event.id)
        
        
@router.post("/addEventLocation")
async def add_card_to_event(event_location: EventLocation):
    location = event_location.location
    location_id = await database.get_location_id(
        location.region,
        location.city_name,
        location.street,
        location.house_number
    )
    event = await database.get_event(event_location.event_name)
    
    if location_id is None:
        raise HTTPException(404, "Location is not exist")
    if event is None:
        raise HTTPException(404, "Event is not exist")
    
    await database.add_location_event(location_id, event.id)        