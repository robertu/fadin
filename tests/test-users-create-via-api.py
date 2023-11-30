import pytest
from django.contrib.auth.models import User
from logging import getLogger

logger = getLogger()


@pytest.mark.django_db(transaction=True)
def test_api_to_orm(asgi_client):
    asgi_client.authorize("admin", is_superuser=True, is_staff=True)
    username = "kokosz"
    response = asgi_client.post("/api/users/", json={"username": username})
    assert response.status_code == 200
    logger.info('created user: %s', username)
    assert response.json()['username'] == username
    assert User.objects.all().count() == 2
    user = User.objects.last()
    logger.info('user retrieved via orm: %s', repr(user))
    assert user.username == username
