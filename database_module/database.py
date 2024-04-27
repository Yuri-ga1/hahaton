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
            
        return client.id if client else None
    
    async def get_card(self, name: str):
        card = self.session.query(Cards)\
            .filter(Cards.name == name)\
            .first()
            
        return card if card else None
    
    async def get_location_id(
        self,
        region: str,
        city: str,
        street: str,
        house_nomber: str
    ):
        location = self.session.query(Location)\
            .filter(
                Location.region == region,
                Location.city_name == city,
                Location.street == street,
                Location.house_number == house_nomber
                )\
            .first()
            
        return location.id if location else None  
    
    async def get_rarity_id(self, name: str):
        rarity = self.session.query(Rarity)\
            .filter(Rarity.name == name)\
            .first()
            
        return rarity.id if rarity else None
        
    
    async def add_device(self, mac: str, location_id: int):
        new_device = Device(
            MAC_address=mac,
            location_id = location_id
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
        
    async def add_location(
        self,
        client_id: int,
        region: str,
        city_name: str,
        street: str,
        house_number: str
    ):
        new_location = Location(
            client_id=client_id,
            region=region,
            city_name=city_name,
            street=street,
            house_number=house_number
        )
        self.session.add(new_location)
        self.session.commit()
        
    
    async def add_location_point(
        self,
        location_id: int,
        longitude: float,
        latitude: float
    ):
        new_locationPoint = LocationPoint(
            location_id=location_id,
            longitude=longitude,
            latitude=latitude
        )
        self.session.add(new_locationPoint)
        self.session.commit()
        
    async def add_rarity(self, rarity: str, chance: float):
        rarity_id = await self.get_rarity_id(rarity)
        if rarity_id is None:
            new_rarity = Rarity(
                name=rarity,
                chance=chance
            )
            self.session.add(new_rarity)
            self.session.commit()
            
    async def add_event(self, name, description):
        new_event = Events(
            name=name,
            description=description
        )
        self.session.add(new_event)
        self.session.commit()
        
    
    async def add_card(
        self,
        name: str,
        type: str,
        rarity_id: int,
        hp: int,
        damage: int,
        speed: int
    ):
        new_card = Cards(
            name=name,
            type=type,
            rarity_id=rarity_id,
            hp=hp,
            damage=damage,
            speed=speed
        )
        self.session.add(new_card)
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
