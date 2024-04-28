from pydantic import BaseModel
from datetime import datetime
from esp_server.esp_hands.schemas import Location

class Event(BaseModel):
    name: str
    description: str
    start: datetime
    end: datetime
    

class Card(BaseModel):
    name: str
    type: str
    rarity: str
    hp: int
    damage: int
    speed: int
    

class Rarity(BaseModel):
    name: str
    chance: float
    

class Type(BaseModel):
    name: str
    dominate: str
    
    
class CardToEvent(BaseModel):
    card_name: str
    event_name: str
    
    
class EventLocation(BaseModel):
    event_name: str
    location: Location