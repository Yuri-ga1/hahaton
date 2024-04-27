from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
from database_module.database import database

from esp_auto.router import router as esp_auto_router
# from esp_hands.router import router as esp_hands_router


app = FastAPI()


app.include_router(esp_auto_router)
# app.include_router(esp_hands_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    

@app.get("/")
async def welcome():
    return {"message": "Hello, world"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
