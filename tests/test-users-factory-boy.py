import pytest
import factory
from django.contrib.auth.models import User
from logging import getLogger

logger = getLogger()

class FakeUserFactory(factory.django.DjangoModelFactory):
    is_staff = True
    is_superuser = False
    username = factory.Faker('name', locale='pl_PL')

    class Meta:
        model = User
        django_get_or_create = ('username',)

class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'John'
    last_name = 'Doe'
    is_staff = True
    is_superuser = False
    username = 'john'

    class Meta:
        model = User
        django_get_or_create = ('username',)

class AdminFactory(factory.django.DjangoModelFactory):
    first_name = 'Admin'
    last_name = 'User'
    is_staff = True
    is_superuser = True
    username = 'admin'

    class Meta:
        model = User
        django_get_or_create = ('username',)


@pytest.mark.django_db(transaction=True)
def test_create_batch(asgi_client):
    asgi_client.authorize("admin", is_superuser=True, is_staff=True)
    FakeUserFactory.create_batch(10)
    response = asgi_client.get("/api/users/count")
    assert response.status_code == 200
    assert response.json() == {"count": 11}
    assert User.objects.all().count() == 11
    for u in User.objects.all():
        logger.info('user retrieved via orm: %s', repr(u))

