from pydantic import BaseModel
from datetime import datetime


class DemandModel(BaseModel):
    DemandRequest = datetime
    DemandedFloor = str
    RequisitedFloor = str
    RestingFloor = str