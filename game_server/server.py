from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio

from database_module.database import database

from game_hands.router import router as game_hands_router

async def _add_rarity():
    basic_rarity = ["Бронза", "Серебро", "Золото"]
    basic_chance = [70, 20, 10]
    for rarity, chance in zip(basic_rarity, basic_chance):
        await database.add_rarity(rarity, chance)
        
async def _add_types():
    types = ['writer', 'historical_figure', 'literary_character']
    dominates = [3, 1, 2]
    for type, slave in zip(types, dominates):
        await database.add_type(type, slave)


app = FastAPI()
app.include_router(game_hands_router)


@app.on_event("startup")
async def startup():
    await database.connect()
    await _add_rarity()
    await _add_types()


@app.on_event("shutdown")
async def shutdown():
    database.disconnect()
    

@app.get("/")
async def get_data():
    return {"message": "Hello, world"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
