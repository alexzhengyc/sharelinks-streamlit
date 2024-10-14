from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Influencer(Base):
    __tablename__ = 'influencers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unique_id = Column(String, unique=True)
    tracking_links = relationship('TrackingLink', back_populates='influencer')

class TrackingLink(Base):
    __tablename__ = 'tracking_links'
    id = Column(Integer, primary_key=True)
    influencer_id = Column(Integer, ForeignKey('influencers.id'))
    destination_url = Column(String)
    unique_code = Column(String, unique=True)
    promo_code = Column(String, unique=True)  # Optional: Include if using promo codes
    influencer = relationship('Influencer', back_populates='tracking_links')
    visits = relationship('Visit', back_populates='tracking_link')

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    tracking_link_id = Column(Integer, ForeignKey('tracking_links.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)
    tracking_link = relationship('TrackingLink', back_populates='visits')
