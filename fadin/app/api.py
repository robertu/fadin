from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/ping", tags=["fun stuff"])
def ping():
    return {"ping": "pong!"}
