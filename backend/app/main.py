from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import missions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def read_healthz():
    return {"status": "ok"}

app.include_router(missions.router)
