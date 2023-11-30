
import pytest
from django.contrib.auth.models import User
from logging import getLogger

logger = getLogger()


username = "admin"
password = "pass"

@pytest.mark.django_db(transaction=True)
def test_login_to_admin(asgi_client, django_user_model):
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=True, is_superuser=True)
    response = asgi_client.get("/admin/login/")
    assert response.status_code == 200
    form_data = {
        "username": username,
        "password": password,
        "csrfmiddlewaretoken":  response.cookies['csrftoken'],
    }
    response = asgi_client.post(
        "/admin/login/",
        data=form_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 200
    assert "Log in | Django site admin" not in response.content.decode()
    response = asgi_client.get("/admin/auth/user/")
    assert response.status_code == 200
    response = asgi_client.get("/admin/ivo/customer/")
    assert response.status_code == 200

@pytest.mark.django_db(transaction=True)
def test_login_to_admin2(asgi_client, django_user_model):
    user = User.objects.create(username=username, password=password, is_staff=True, is_superuser=True)
    response = asgi_client.get("/admin/auth/user/")
    assert response.status_code == 200
