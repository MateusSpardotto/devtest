from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Demand(Base):
    __tablename__ = 'demands'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    DemandRequest = Column(DateTime, nullable=False)
    DemandedFloor = Column(String(255), nullable=False)
    RequisitedFloor = Column(String(255), nullable=False)
    RestingFloor = Column(String(255), nullable=False)

