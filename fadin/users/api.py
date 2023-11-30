from datetime import datetime
from logging import getLogger

from django.contrib.auth.models import User
from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel

from app.api import router as app_router
from app.auth import is_loggedin, perm, request_user
from app.exceptions import AuthException

logger = getLogger()

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(is_loggedin)])


class UserModelCreate(BaseModel):
    username: str
    first_name: str = ""
    last_name: str = ""
    email: str = ""


class UserModelList(BaseModel):
    id: int
    username: str
    email: str


class UserModelGet(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    date_joined: datetime
    last_login: datetime | None
    is_superuser: bool
    is_staff: bool
    is_active: bool


class CounterModel(BaseModel):
    count: int


@router.post("/", dependencies=[Depends(perm("auth.add_user"))])
def create_user(
    data: UserModelCreate,
) -> UserModelGet:
    created = User.objects.create(**data.model_dump())
    return created


@router.get("/", status_code=200)
def get_users(limit: int = 10, offset: int = 0) -> list[UserModelList]:
    objects = User.objects.all()[offset : offset + limit]
    return list(objects)


@router.get("/count", dependencies=[Depends(perm("auth.view_user"))])
def get_users_count() -> CounterModel:
    return CounterModel(count=User.objects.count())


@router.get("/{pk}", response_model=UserModelGet)
def get_user(pk: int):
    return User.objects.get(pk=pk)


app_router.include_router(router)
