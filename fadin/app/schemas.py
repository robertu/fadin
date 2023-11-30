from typing import Dict, Generic, List, Optional, Sequence, TypeVar

from django.db import models
from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    @classmethod
    def from_orms(cls, instances: List[models.Model]):
        return [cls.from_orm(inst) for inst in instances]


class PaginatedResponse(BaseModel, Generic[T]):
    next: bool
    prev: bool
    count: int
    offset: int
    limit: int
    data: List[T]

    @classmethod
    def create(
        cls,
        *,
        next: bool,
        prev: bool,
        count: int,
        offset: int,
        limit: int,
        data: Sequence[T],
        schema: BaseModel,
        **kwargs: Dict,
    ):
        return cls(
            next=next,
            prev=prev,
            count=count,
            offset=offset,
            limit=limit,
            data=schema.from_orms(data),
            **kwargs,
        )

    class Config:
        schema_extra = {
            "example": {
                "next": True,
                "prev": True,
                "count": 3,
                "offset": 0,
                "limit": 100,
                "data": [{}, {}, {}],
            }
        }


def get_next(count=0, offset=0, limit=100):
    return


def get_previous(offset=0):
    return


def get_paginated_response(
    offset=0, limit=100, model=models.Model, schema=BaseModel, filter={}
) -> PaginatedResponse[BaseModel]:
    if isinstance(filter, models.Q):
        qs = model.objects.filter(filter)
    elif isinstance(filter, dict):
        qs = model.objects.filter(**filter)
    count = qs.count()
    data = qs[offset : (offset + limit)]
    has_next = count > offset + limit
    has_prev = offset > 0
    return PaginatedResponse.create(
        next=has_next,
        prev=has_prev,
        count=count,
        offset=offset,
        limit=limit,
        data=data,
        schema=schema,
    )
