from pydantic import BaseModel
from typing import List


class Client(BaseModel):
    name: str
    lastname: str
    email: str
    
    
class Location(BaseModel):
    client_email: str
    region: str
    city_name: str
    street: str
    house_number: str
    

class LocationPoints(BaseModel):
    location: Location
    longitude: List[float]
    latitude: List[float]