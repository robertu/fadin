import pytest
from django.http import HttpResponseRedirect
from logging import getLogger

logger = getLogger()


def test_with_admin_user(client, django_user_model):
    username = "admin2"
    password = "password2"
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=True, is_superuser=True)
    client.force_login(user)
    response = client.get('/admin/')
    assert 'Site administration' in response.content.decode('utf-8')

def test_with_staff_user(client, django_user_model):
    username = "user"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=True, is_superuser=False)
    client.force_login(user)
    response = client.get('/admin/')
    assert 'Site administration' in response.content.decode('utf-8')

def test_with_regular_user(client, django_user_model):
    username = "user"
    password = "password"
    user = django_user_model.objects.create_user(username=username, password=password, is_staff=False, is_superuser=False)
    client.force_login(user)
    response = client.get('/admin/')
    assert type(response) == HttpResponseRedirect
    assert response.status_code == 302

def test_get_users(test_user, django_user_model):
    # the user object should be included in this queryset
    all_users = django_user_model.objects.all()
    assert all_users.count() == 4

def test_with_test_user(client, test_user, django_user_model):
    for u in django_user_model.objects.all():
        logger.info(f'user: {u.id} {u.username}')
    user = django_user_model.objects.get(username="test_user")
    client.force_login(user)
    response = client.get('/admin/')
    assert response.status_code == 302
