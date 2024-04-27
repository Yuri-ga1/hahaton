from pydantic import BaseModel

class Event(BaseModel):
    name: str
    description: str
    

class Card(BaseModel):
    name: str
    type: str
    rarity: str
    hp: int
    damage: int
    speed: int