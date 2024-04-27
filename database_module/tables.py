from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    
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
    client = relationship('Client', back_populates='locations')

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    MAC_address = Column(String, nullable=False)
    # location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    
    data = relationship('Data', back_populates='device')
    # location = relationship('Location', back_populates='devices')

class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    PM2_5 = Column(Float, nullable=False)
    PM10 = Column(Float, nullable=False)
    # temperature = Column(Float, nullable=False)
    # humidity = Column(Float, nullable=False)
    
    device = relationship('Device', back_populates='data')

class LocationPoint(Base):
    __tablename__ = 'location_points'

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    
    location = relationship('Location', back_populates='location_points')

class Card(Base):
    __tablename__ = 'card'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(Enum('writer', 'historical_figure', 'literary_character'), nullable=False)
    rarity_id = Column(Integer, ForeignKey('chance_rarity.id'), nullable=False)
    hp = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    
    cards = relationship('PlayerCards', back_populates='card')
    raritytable = relationship('Rarity', back_populates='rarity')
    
    
class Player(Base):
    __tablename__ = 'player'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    login = Column(String, nullable=False)
    
    players = relationship('PlayerCards', back_populates='player')
    
class PlayerCards(Base):
    __tablename__ = 'player_cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)
    count = Column(Integer, nullable=False)
    
    player = relationship('Player', back_populates='players')
    card = relationship('Card', back_populates='cards')
    
class CardTypes(Base):
    __tablename__ = 'card_types'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
class Events(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    events = relationship('CardEvent', back_populates='event')
    
    
class CardsEvent(Base):
    __tablename__ = 'cards_event'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    card_id = Column(Integer, ForeignKey('card.id'), nullable=False)
    
    event = relationship('Events', back_populates='events')
    card = relationship('Card', back_populates='cards')
    

class Rarity(Base):
    __tablename__ = 'chance_rarity'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chance = Column(Integer, nullable=False)
    
    rarity = relationship('Card', back_populates='raritytable')
    
class LocationEvent(Base):
    __tablename__ = 'location_event'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    locations_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    events_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    
    event = relationship('Events', back_populates='events')
    location = relationship('Location', back_populates='location_points')
 