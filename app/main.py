from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from itertools import count

app = FastAPI()


class Status(str, Enum):
    invited = "invited"
    confirmed = "confirmed"
    declined = "declined"
    tentative = "tentative"


class Assignment(BaseModel):
    id: int
    mission_id: int
    user_id: Optional[int] = None
    role_label: str
    status: Status


class AssignmentIn(BaseModel):
    role_label: str
    user_id: Optional[int] = None
    status: Optional[Status] = Status.invited


class Position(BaseModel):
    label: str
    count: int


class Mission(BaseModel):
    id: int
    positions: List[Position]
    assignments: List[Assignment] = []


missions: Dict[int, Mission] = {}
_assignment_id = count(1)


@app.post("/missions/{mid}/assign", response_model=Assignment)
def assign(mid: int, payload: AssignmentIn) -> Assignment:
    mission = missions.get(mid)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    position = next((p for p in mission.positions if p.label == payload.role_label), None)
    if position is None:
        raise HTTPException(status_code=422, detail="Invalid role")

    existing = [a for a in mission.assignments if a.role_label == payload.role_label]
    if len(existing) >= position.count:
        raise HTTPException(status_code=422, detail="Role capacity exceeded")

    assignment = Assignment(
        id=next(_assignment_id),
        mission_id=mid,
        user_id=payload.user_id,
        role_label=payload.role_label,
        status=payload.status or Status.invited,
    )
    mission.assignments.append(assignment)
    return assignment
