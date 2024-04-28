from pydantic import BaseModel


class Player(BaseModel):
    nickname: str
    login: str
    

class PlayerCard(BaseModel):
    player_nickname: str
    card_name: str
    count: int