import pytest
from starlette.testclient import TestClient
from app.asgi import application
from django.core.management import call_command
from ivo.models import Invoice, Customer, Company, Item, InvoiceItem

from django.contrib.auth.models import User
class AuthorizedTestClient(TestClient):

    def authorize(self, username="admin", is_superuser=True, is_staff=True, password="password"):
        User.objects.create_user(username=username, password=password, is_staff=is_staff, is_superuser=is_superuser)
        response = self.get("/admin/login/")
        assert response.status_code == 200
        form_data = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken":  response.cookies['csrftoken'],
        }
        response = self.post(
            "/admin/login/",
            data=form_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        assert response.status_code == 200
        assert "Log in | Django site admin" not in response.content.decode()

@pytest.fixture(scope="session")
def asgi_client():
    client = AuthorizedTestClient(application)
    yield client


fixtures = ['fix/auth.json', 'fix/ivo.json',]

@pytest.fixture(autouse=True, scope='session')
def django_fixtures_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', *fixtures)

@pytest.fixture
def test_user(django_user_model):
    return django_user_model.objects.get_or_create(username="test_user", password="password")

@pytest.fixture
def test_invoice():
    buyer = Customer.objects.create(name="Kopalnia Kruszywa S.A.", address="ul. Kocińska 21", taxid="12345678")
    seller = Company.objects.create(name="PyKonik LTD", address="Kraków", taxid="00110011")
    invoice = Invoice.objects.create(buyer=buyer, seller=seller, number="2021/01/0001")
    return invoice


