from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from elevators.infra import infra_database
from elevators.models.demand_model import DemandModel
from elevators.models.demand_range_response import DemandRangeResponse
from elevators.models.range_demands_modl import RangeDemandModel
from elevators.sql_documents.demand import Demand


router = APIRouter()

@router.post("/CreateDemand/", response_model=DemandModel)#TODO: Colocar todos os models em um arquivo só para simplificar
def create_demand(demand: DemandModel, db: Session = Depends(infra_database.get_db)):
    try:
        db_demand = Demand(**demand.dict())
        db.add(db_demand)
        db.commit()
        db.refresh(db_demand)
        return JSONResponse(status_code=200, content=db_demand)
    except Exception as e:
        return HTTPException(status_code=500, details=e)

@router.get("/demands/", response_model=List[DemandModel])
def get_demands(db: Session = Depends(infra_database.get_db)):
    try:
        demands = db.query(Demand).all()
        return JSONResponse(status_code=200, content=demands)
    except Exception as e:
        return HTTPException(status_code=500, details=e)
    
@router.get("/demands/range", response_model=DemandRangeResponse)
def get_demands(range = RangeDemandModel, db: Session = Depends(infra_database.get_db)):
    try:
        demands = db.query(Demand).filter(
        DemandModel.DemandRequest >= range.StartDate,
        DemandModel.DemandRequest <= range.EndDate
        ).all()
    
        demand_responses = [
            DemandModel(
                DemandRequest=demand.DemandRequest,
                DemandedFloor=demand.DemandedFloor,
                RequisitedFloor=demand.RequisitedFloor,
                RestingFloor=demand.RestingFloor
            ) for demand in demands
        ]
        
        dataDemandRange = f"{range.StartDate} - {range.EndDate}"
        return JSONResponse(status_code=200, content=DemandRangeResponse(dataDemandRange=dataDemandRange, demands=demand_responses))
    except Exception as e:
        return HTTPException(status_code=500, details=e)