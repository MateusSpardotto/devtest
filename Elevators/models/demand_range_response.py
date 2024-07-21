from pydantic import BaseModel
from typing import List
from elevators.models.demand_model import DemandModel


class DemandRangeResponse(BaseModel):
    dataDemandRange: str
    demands: List[DemandModel]