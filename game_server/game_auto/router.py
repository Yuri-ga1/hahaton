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
    
    
