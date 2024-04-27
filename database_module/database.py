from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

from .tables import *

class Database:

    def __init__(self, db_name: str = "DATABASE"):
        self.db_name = db_name
        self.session = None

    async def connect(self):
        print("create connection")
        engine = create_engine(f'sqlite:///{self.db_name}.db')
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        self.session = Session()
        
        
    async def disconnect(self):
        print("disconnect")
        self.session.close()


    async def get_device_by_mac(self, mac: str):
        device = self.session.query(Device)\
            .filter(Device.MAC_address == mac)\
            .first()
        
        return device.id if device else None
        
        
    async def get_client_by_email(self, email: str):
        client = self.session.query(Client)\
            .filter(Client.email == email)\
            .first()
            
        return client.email if client else None
        
    
    async def add_device(self, mac: str):
        new_device = Device(
            MAC_address=mac
        )
        self.session.add(new_device)
        self.session.commit()
        
    async def add_client(self, name: str, lastname: str, email: str):
        new_client = Client(
            name=name,
            lastname=lastname,
            email=email
        )
        self.session.add(new_client)
        self.session.commit()

    async def save_data(
        self,
        device_id: int,
        pmtwo: float,
        pm10: float,
        humidity: float,
        celsius: float,
        fahrenheit: int,
        date: datetime = datetime.now()
    ):
        new_data = Data(
            device_id=device_id,
            date=date,
            PM2_5=pmtwo,
            PM10=pm10,
            humidity=humidity,
            celsius=celsius,
            fahrenheit=fahrenheit
        )
        self.session.add(new_data)
        self.session.commit()
        


database = Database()
