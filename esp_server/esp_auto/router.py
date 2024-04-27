from fastapi import APIRouter, HTTPException
from database_module.database import database
from datetime import datetime
from .schemas import *

router = APIRouter()

@router.post("/dataReceiver")
async def data_receiver(data: ESP_data):
    date = datetime.fromtimestamp(data.date)
    device_id = await database.get_device_by_mac(data.mac)
    if device_id:
       await database.save_data(
            device_id=device_id,
            pmtwo=data.pm2_5,
            pm10=data.pm10,
            humidity=data.hum,
            fahrenheit=data.fahr,
            celsius=data.cel,
            date=date
        )
    else: 
        return HTTPException(404, "Device is not registered")
       
@router.post("/registerDevice")
async def register_device(mac: dict):
    if (len(mac) != 1 and "mac" not in mac):
        return HTTPException(422, detail="Invalid data format")
    
    mac_address = mac['mac']
    
    device = await database.get_device_by_mac(mac_address)
    if device is None:
        await database.add_device(mac_address)
    else:
        return HTTPException(409, detail="Device alredy exists")