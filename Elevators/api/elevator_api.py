from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Elevators.infra import infraDatabase
from Elevators.models import demandCreated
from Elevators.sqlDocuments.demand import Demand


router = APIRouter()

@router.post("/demands/", response_model=demandCreated.DemandCreate)
def create_demand(demand: demandCreated.DemandCreate, db: Session = Depends(infraDatabase.get_db)):
    db_demand = Demand(**demand.dict())
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand

@router.get("/demands/", response_model=List[demandCreated.DemandCreate])
def get_demands(db: Session = Depends(infraDatabase.get_db)):
    demands = db.query(Demand).all()
    return demands