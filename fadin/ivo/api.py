from datetime import datetime
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from asgiref.sync import sync_to_async
from app.api import router as app_router

from .models import Invoice

router = APIRouter(prefix="/ivo", tags=["ivo"])


class CustomerModel(BaseModel):
    name: str
    address: str
    taxid: str


class CompanyModel(BaseModel):
    name: str
    address: str
    taxid: str

class InvoiceItemGet(BaseModel):
    item_id: int
    price: float
    amount: float
class InvoiceItem4CreateInvoice(BaseModel):
    item_id: int = 1
    price: float | None
    quantity: int = 1

class InvoiceModelGet(BaseModel):
    number: str
    created_at: datetime
    # amount: float
    buyer: CustomerModel
    seller: CompanyModel

class InvoiceModelCreate(BaseModel):
    buyer_id: int
    seller_id: int
    items: List[InvoiceItem4CreateInvoice]

class InvoiceModelFull(BaseModel):
    number: str
    created_at: datetime
    buyer_id: int
    seller_id: int
    created_at: datetime
    amount: float
    items: List[InvoiceItemGet]


@router.get("/invoices", status_code=200)
def get_invoices(limit: int = 10, offset: int = 0) -> list[InvoiceModelGet]:
    objects = Invoice.objects.all()[offset : offset + limit]
    return list(objects)

@sync_to_async
def get_inv(pk: int) -> InvoiceModelFull:
    invoice = Invoice.objects.get(pk=pk)
    invoice.items = list(invoice.invoiceitem_set.all())
    return invoice

# @router.post("/invoice", status_code=200)
# async def create_invoice(data: InvoiceModelCreate) -> InvoiceModelFull:
#     invoice = await Invoice.new(**data.model_dump())
#     return await get_inv(invoice.pk)


@router.get("/invoice/{pk}", status_code=200)
async def get_invoice(pk: int) -> InvoiceModelFull:
    return await get_inv(pk)

app_router.include_router(router)
