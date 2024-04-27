from pydantic import BaseModel


class ESP_data(BaseModel):
    mac: str
    date: int
    pTwo_Half: float
    p10: float
    # temperature: float
    # humidity: float
