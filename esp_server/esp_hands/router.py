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
        raise HTTPException(409, detail="Client alredy exists")
    else:
        await database.add_client(
            client.name,
            client.lastname,
            client.email
        )
    
    

    

@router.post("/addClientLocation")
async def add_client_location(location: Location):
    if not validate_email(location.client_email):
        raise HTTPException(400, "Invalid email address")
    
    client_id = await database.get_client_by_email(location.client_email)
    if client_id:
        await database.add_location(
            client_id=client_id,
            region=location.region,
            city_name=location.city_name,
            street=location.street,
            house_number = location.house_number
        )
    else:
        raise HTTPException(404, "Client is not exist")