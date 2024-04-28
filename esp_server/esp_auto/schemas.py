from pydantic import BaseModel


class MacAddress(BaseModel):
    mac: str


class ESP_data(BaseModel):
    mac: str
    date: int
    pm2_5: float
    pm10: float
    hum: float
    cel: float
    fahr: int
