from pydantic import BaseModel


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