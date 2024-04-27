from fastapi import APIRouter, HTTPException
from .schemas import *
from database_module.database import database
from validate_email_address import validate_email


router = APIRouter()


@router.post("/addClient")
async def add_client(client: Client):
    if not validate_email(client.email):
        raise HTTPException(400, "Invalid email address")
    
    if await database.get_client_by_email(client.email):
        return HTTPException(409, detail="Client alredy exists")
    else:
        await database.add_client(
            client.name,
            client.lastname,
            client.email
        )
    
    

    

@router.post("/merge")
async def router_merge():
    pass