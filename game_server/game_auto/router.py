from fastapi import APIRouter, HTTPException
import asyncio
from .schemas import *
from database_module.database import database

router = APIRouter()

@router.post("/addPlayer")
async def create_player(player: Player):
    old_player = await database.get_player(player.nickname)
    if old_player:
        raise HTTPException(409, detail=f"Player {player.nickname} alredy exists")
    else:
        await database.add_player(player.nickname, player.login)
    

@router.post("/addPlayerCard")
async def create_player(player_card: PlayerCard):
    card = await database.get_card(player_card.card_name)
    player = await database.get_player(player_card.player_nickname)
    
    if card is None:
        raise HTTPException(404, f"Card {player_card.card_name} is not exist")
    if player is None:
        raise HTTPException(404, f"Player {player_card.player_nickname} is not exist")
    
    player_id = player.id
    card_id = card.id
    player_cards = await database.get_player_cards(player_id, card_id)
    
    if player_cards:
        await database.update_player_card_count(player_id, card_id, player_card.count)
    else:
        await database.add_player_card(player_id, card_id, player_card.count)
        
