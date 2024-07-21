from pydantic import BaseModel, field_validator
from datetime import datetime


class RangeDemandModel(BaseModel):
    StartDate: datetime
    EndDate: datetime

    @field_validator("StartDate", "EndDate")
    def validate_range_demand(cls, start_date, end_date):
        if start_date > end_date:
            raise ValueError(f"Invalid range date: Start date - {start_date} and End date - {end_date}")
        
        return True

    