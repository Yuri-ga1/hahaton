from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


card_event_association = Table(
    'cards_event', Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", Integer, ForeignKey('events.id'), nullable=False),
    Column("card_id", Integer, ForeignKey('cards.id'), nullable=False)
)  


player_card_association = Table(
    'player_card', Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", Integer, ForeignKey('player.id'), nullable=False),
    Column("card_id", Integer, ForeignKey('cards.id'), nullable=False),
    Column("count", Integer, nullable=False)
)   


location_event_association = Table(
    'location_event', Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("locations_id", Integer, ForeignKey('locations.id'), nullable=False),
    Column("events_id", Integer, ForeignKey('events.id'), nullable=False)
)   


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    locations = relationship('Location', back_populates='client')

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    region = Column(String, nullable=False)
    city_name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    
    devices = relationship('Device', back_populates='location')
    event_location = relationship("Events", secondary=location_event_association, back_populates="location_event")
    client = relationship('Client', back_populates='locations')
    location_points = relationship('LocationPoint', back_populates='location')

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    MAC_address = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    
    data = relationship('Data', back_populates='device')
    location = relationship('Location', back_populates='devices')

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    PM2_5 = Column(Float, nullable=False)
    PM10 = Column(Float, nullable=False)
    fahrenheit = Column(Integer, nullable=False)
    celsius = Column(Integer, nullable=False)
    humidity = Column(Integer, nullable=False)
    
    device = relationship('Device', back_populates='data')

class LocationPoint(Base):
    __tablename__ = 'location_points'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    
    location = relationship('Location', back_populates='location_points')

class Cards(Base):
    __tablename__ = 'cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('writer', 'historical_figure', 'literary_character'), nullable=False)
    rarity_id = Column(Integer, ForeignKey('rarity.id'), nullable=False)
    hp = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    
    cards = relationship('Player', secondary=player_card_association, back_populates='players')
    events = relationship('Events', secondary=card_event_association, back_populates='event_cards')
    raritytable = relationship('Rarity', back_populates='rarity')
    
    
class Player(Base):
    __tablename__ = 'player'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nikcname = Column(String, nullable=False)
    login = Column(String, nullable=False)
    
    players = relationship('Cards', secondary=player_card_association, back_populates='cards')
    
  
class Events(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    event_cards = relationship('Cards', secondary=card_event_association, back_populates='events')
    location_event = relationship('Location', secondary=location_event_association, back_populates='event_location')
    

class Rarity(Base):
    __tablename__ = 'rarity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chance = Column(Float, nullable=False)
    
    rarity = relationship('Cards', back_populates='raritytable')
