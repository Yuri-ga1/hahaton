from fastapi import APIRouter
from .schemas import *
from typing import List
from database_module.database import database


router = APIRouter()


@router.post("/download_data")
async def download_data():
    pass
    

@router.post("/merge")
async def router_merge():
    pass