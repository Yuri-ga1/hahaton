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
    
    
@router.post("/addLocationPoints")
async def add_location_points(location_poins: LocationPoints):
    location: Location = location_poins.location
    location_id = await database.get_location_id(
        location.region,
        location.city_name,
        location.street,
        location.house_number
    )
    
    if len(location_poins.longitude) != len(location_poins.latitude):
        raise HTTPException(400, "Invalid points format")
    
    if location_id:
        for longitude, latitude in zip(location_poins.longitude, location_poins.latitude):
            await database.add_location_point(
                location_id=location_id,
                longitude=longitude,
                latitude=latitude
            )
    else:
        raise HTTPException(404, "Location is not exist")
        
    