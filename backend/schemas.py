from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict

from pydantic import BaseModel, Field, validator, root_validator

UTC_PLUS_4 = timezone(timedelta(hours=4))


class Position(BaseModel):
    label: str
    count: int = Field(..., ge=1)
    skills: Dict[str, str] = Field(default_factory=dict)


class MissionBase(BaseModel):
    title: str
    start: datetime
    end: datetime
    location: Optional[str] = None
    status: str = Field("draft", regex="^(draft|published)$")
    positions: List[Position] = Field(default_factory=list)

    @validator("start", "end", pre=True)
    def ensure_timezone(cls, v):
        # Parse string and set default timezone to UTC+4 if none
        if isinstance(v, str):
            dt = datetime.fromisoformat(v)
        else:
            dt = v
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC_PLUS_4)
        return dt

    @root_validator
    def check_dates(cls, values):
        start = values.get("start")
        end = values.get("end")
        if start and end and not start < end:
            raise ValueError("start must be before end")
        return values


class MissionCreate(MissionBase):
    pass


class MissionUpdate(MissionBase):
    pass


class Mission(MissionBase):
    id: int

    class Config:
        orm_mode = True
