from pydantic import BaseModel


class DemandResponseModel(BaseModel):
    DemandRequest: str
    DemandedFloor: str
    RequisitedFloor: str
    RestingFloor: str