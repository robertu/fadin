import pytest

@pytest.mark.django_db(transaction=True)
def test_get_users_count(asgi_client):
    asgi_client.authorize("admin", is_superuser=True, is_staff=True)
    response = asgi_client.get("/api/users/count")
    assert response.status_code == 200
    assert response.json() == {"count": 1}

