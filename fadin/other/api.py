from fastapi import APIRouter, Request

from app.api import router as app_router

router = APIRouter(prefix="/other", tags=["other"])


@router.get("/other")
def ping(r: Request):
    return {"other": f"stuff... request user_id is {r.state.user}"}


app_router.include_router(router)
