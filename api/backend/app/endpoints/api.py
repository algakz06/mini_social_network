from os import walk
from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)
