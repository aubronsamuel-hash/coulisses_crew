from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from .schemas import Mission, MissionCreate, MissionUpdate

app = FastAPI()

# In-memory storage
MISSIONS: List[Mission] = []
NEXT_ID = 1


def apply_filters(
    missions: List[Mission],
    q: Optional[str],
    status: Optional[str],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    role: Optional[str],
):
    result = missions
    if q:
        result = [m for m in result if q.lower() in m.title.lower()]
    if status:
        result = [m for m in result if m.status == status]
    if date_from:
        result = [m for m in result if m.start >= date_from]
    if date_to:
        result = [m for m in result if m.end <= date_to]
    if role:
        result = [m for m in result if any(p.label == role for p in m.positions)]
    return result


@app.get("/missions", response_model=List[Mission])
def list_missions(
    q: Optional[str] = None,
    status: Optional[str] = Query(None, regex="^(draft|published)$"),
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    role: Optional[str] = None,
    page: int = 1,
    per_page: int = 10,
):
    missions = apply_filters(MISSIONS, q, status, date_from, date_to, role)
    start = (page - 1) * per_page
    end = start + per_page
    return missions[start:end]


@app.post("/missions", response_model=Mission, status_code=201)
def create_mission(mission: MissionCreate):
    global NEXT_ID
    mission_data = Mission(id=NEXT_ID, **mission.dict())
    MISSIONS.append(mission_data)
    NEXT_ID += 1
    return mission_data


@app.get("/missions/{mission_id}", response_model=Mission)
def get_mission(mission_id: int):
    for m in MISSIONS:
        if m.id == mission_id:
            return m
    raise HTTPException(status_code=404, detail="Mission not found")


@app.put("/missions/{mission_id}", response_model=Mission)
def update_mission(mission_id: int, mission: MissionUpdate):
    for idx, m in enumerate(MISSIONS):
        if m.id == mission_id:
            updated = Mission(id=mission_id, **mission.dict())
            MISSIONS[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Mission not found")


@app.delete("/missions/{mission_id}", status_code=204)
def delete_mission(mission_id: int):
    for idx, m in enumerate(MISSIONS):
        if m.id == mission_id:
            del MISSIONS[idx]
            return
    raise HTTPException(status_code=404, detail="Mission not found")
