import pytest


@pytest.mark.django_db(transaction=True)
def test_ping(asgi_client):
    response = asgi_client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}