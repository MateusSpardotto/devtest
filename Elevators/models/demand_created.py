from pydantic import BaseModel
from datetime import datetime


class DemandCreate(BaseModel):
    DemandHour: datetime
    FloorDemand: str
    RequisitedFloor: str