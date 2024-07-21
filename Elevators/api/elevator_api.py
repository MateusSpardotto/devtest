from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from elevators.infra import infraDatabase
from elevators.models import demandCreated
from elevators.sqlDocuments.demand import Demand


router = APIRouter()

@router.post("/demands/", response_model=demandCreated.DemandCreate)
def create_demand(demand: demandCreated.DemandCreate, db: Session = Depends(infraDatabase.get_db)):
    try:
        db_demand = Demand(**demand.dict())
        db.add(db_demand)
        db.commit()
        db.refresh(db_demand)
        return JSONResponse(status_code=200, content=db_demand)
    except Exception as e:
        return HTTPException(status_code=500, details=e)

@router.get("/demands/", response_model=List[demandCreated.DemandCreate])
def get_demands(db: Session = Depends(infraDatabase.get_db)):
    try:
        demands = db.query(Demand).all()
        return JSONResponse(status_code=200, content=demands)
    except Exception as e:
        return HTTPException(status_code=500, details=e)