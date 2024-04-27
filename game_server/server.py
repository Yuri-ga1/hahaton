from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
from database_module.database import database

from sites.router import router as sites_router
from data_worker.router import router as data_worker_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    database.connect()


@app.on_event("shutdown")
async def shutdown():
    database.disconnect()
    

@app.get("/")
async def get_data():
    return {"message": "Hello, world"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
