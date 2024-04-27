from fastapi import APIRouter, HTTPException
from database_module.database import database
from datetime import datetime
from .schemas import *

router = APIRouter()

@router.post("/dataReceiver")
async def data_receiver(data: ESP_data):
    date = datetime.fromtimestamp(data.date)
    device_id = await database.get_id_by_mac(data.mac)
    if device_id:
        database.save_data(
            device_id,
            data.pTwo_Half,
            data.p10,
            # data.temperature,
            # data.humidity,
            date
        )
    else: 
        HTTPException(404, "Device is not registered")
       
@router.post("/registerDevice")
async def register_device(mac: str):
    device = database.get_id_by_mac(mac)
    if device is None:
        database.add_device(mac)
    # else:
        # HTTPException(409, detail="Device alredy exists")