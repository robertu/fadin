from logging import getLogger

from django.contrib.auth.models import User
from fastapi import Depends, Request

from app.exceptions import AuthException

logger = getLogger()


def request_user(r: Request) -> User:
    return r.state.user


def is_loggedin(r: Request):
    if r.state.user is not None and r.state.user.is_authenticated:
        return True
    raise AuthException("Not logged in.")


def perm(perm_name: str):
    def _perm(user: User = Depends(request_user)):
        if user.has_perm(perm_name):
            return True
        logger.error(
            f'Permission denied for user {user.username}, perm: "{perm_name}".'
        )
        raise AuthException(f"Permission denied.")

    return _perm
