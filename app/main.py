"""Application entry point for the FastAPI backend."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth import router as auth_router


load_dotenv()

app = FastAPI()

origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
