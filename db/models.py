from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Race(Base):
    __tablename__ = "races"
    id = Column(Integer, primary_key=True)
    bookmaker = Column(String)
    race_name = Column(String)
    race_start = Column(String)  # can adjust to TIMESTAMP if parsing times
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)

class Horse(Base):
    __tablename__ = "horses"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Runner(Base):
    __tablename__ = "runners"
    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey("races.id"))
    horse_id = Column(Integer, ForeignKey("horses.id"))
    horse_name = Column(String)

class Odds(Base):
    __tablename__ = "odds"
    id = Column(Integer, primary_key=True)
    runner_id = Column(Integer, ForeignKey("runners.id"))
    bookmaker = Column(String)
    odds_decimal = Column(Numeric)
    odds_raw = Column(String)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
