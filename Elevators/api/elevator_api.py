from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from elevators.infra import infra_database
from elevators.models.demand_model import DemandModel
from elevators.models.demand_response_model import DemandResponseModel
from elevators.sql_documents.demand import Demand


router = APIRouter()

@router.post("/CreateDemand/", response_model=DemandModel)
def create_demand(demand: DemandModel, db: Session = Depends(infra_database.get_db)):
    try:
        db_demand = Demand(**demand.dict())
        db.add(db_demand)
        db.commit()
        db.refresh(db_demand)

        return JSONResponse(status_code=200, content=db_demand)
    except Exception as e:
        return HTTPException(status_code=500, details=e)

@router.get("/demands/", response_model=List[DemandResponseModel])
def get_demands(db: Session = Depends(infra_database.get_db)):
    try:
        demands = db.query(Demand).all()
        resposne = []

        for demand in demands:
            demand_model = DemandResponseModel(
                DemandRequest= demand.DemandRequest.strftime("%m-%d-%Y %H:%M:%S"),
                RequisitedFloor= demand.RequisitedFloor,
                DemandedFloor= demand.DemandedFloor,
                RestingFloor= demand.RestingFloor
            ).model_dump()

            resposne.append(demand_model)
        
        return JSONResponse(status_code=200, content=resposne)
    except Exception as e:
        return HTTPException(status_code=500, details=e)
    
@router.get("/demands/range")
def get_demands(StartDate: datetime, EndDate: datetime, db: Session = Depends(infra_database.get_db)):
    try:
        demands = db.query(Demand).filter(
        Demand.DemandRequest >= StartDate,
        Demand.DemandRequest <= EndDate
        ).all()
    
        demand_responses = []
        for demand in demands:
            demand_model = DemandResponseModel(
                DemandRequest= demand.DemandRequest.strftime("%m-%d-%Y %H:%M:%S"),
                RequisitedFloor= demand.RequisitedFloor,
                DemandedFloor= demand.DemandedFloor,
                RestingFloor= demand.RestingFloor
            ).model_dump()
            demand_responses.append(demand_model)
        
        dataDemandRange = f"{StartDate} - {EndDate}"
        response ={"DemandRange": dataDemandRange,
                   "Demands": demand_responses}
        
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return HTTPException(status_code=500, details=e)
    