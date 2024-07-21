from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Demand(Base):
    __tablename__ = 'demands'
    DemandRequest = Column(DateTime, primary_key=True)
    DemandedFloor = Column(String(255))
    RequisitedFloor = Column(String(255))
    RestingFloor = Column(String(255))

