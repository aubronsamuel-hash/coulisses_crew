from fastapi import APIRouter

from .. import storage

router = APIRouter()


@router.get("/missions")
def get_missions():
    return storage.read_data()
