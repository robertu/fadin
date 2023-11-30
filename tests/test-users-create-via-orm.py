import pytest
from django.contrib.auth.models import User
from logging import getLogger

logger = getLogger()

@pytest.mark.django_db(transaction=True)
def test_orm_to_api(asgi_client):
    asgi_client.authorize("admin", is_superuser=True, is_staff=True)
    user = User.objects.create(username='kajko')
    response = asgi_client.get(f"/api/users/{user.pk}")
    response_obj = response.json()
    assert response.status_code == 200
    logger.info(str(User.objects.all()))
    logger.info('retrieved user: %s', response_obj['username'])
    assert response_obj["username"] == user.username
