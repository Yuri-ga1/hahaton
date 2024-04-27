from pydantic import BaseModel


class Client(BaseModel):
    name: str
    lastname: str
    email: str