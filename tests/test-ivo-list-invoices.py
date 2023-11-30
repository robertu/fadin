import pytest
from django.contrib.auth.models import User
from ivo.models import Invoice
from logging import getLogger

logger = getLogger()


@pytest.mark.django_db(transaction=True)
def test_list_invoices(asgi_client, test_invoice, test_user):
    response = asgi_client.get("/api/ivo/invoices")
    assert response.status_code == 200
    invoices = response.json()
    for i in invoices:
        logger.info('invoice: %s', i)
    assert Invoice.objects.all().count() == len(invoices)
