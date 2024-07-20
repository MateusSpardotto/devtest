from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Demand(Base):
    __tablename__ = 'demands'
    DemandHour = Column(DateTime, primary_key=True)
    FloorDemand = Column(String(255))
    RequisitedFloor = Column(String(255))
