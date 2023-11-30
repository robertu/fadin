import os
from importlib import import_module
from logging import getLogger

from fastapi import FastAPI, Request

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")  # noqa

from asgiref.sync import sync_to_async
from django.apps import apps
from django.conf import settings
from django.core.asgi import get_asgi_application

from .api import router
from .exceptions import unhandled_exception_handler

apps.populate(settings.INSTALLED_APPS)

from django.contrib.auth.models import AnonymousUser, User

logger = getLogger()

application = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    prefix="/api",
    title="fadin API",
    description=f"fadin {settings.VERSION}",
    version=settings.VERSION,
    openapi_url="/api/openapi.json",
)


@sync_to_async
def get_user_from_session(session):
    pk = session.get("_auth_user_id")
    try:
        return User.objects.get(pk=pk, is_active=True)
    except User.DoesNotExist:
        return AnonymousUser()


@application.middleware("http")
async def extend_state(request: Request, call_next):
    engine = import_module(settings.SESSION_ENGINE)
    session_key = request.cookies.get(settings.SESSION_COOKIE_NAME)
    session = engine.SessionStore(session_key)
    accessed = session.accessed  # noqa: F841
    modified = session.modified  # noqa: F841
    empty = session.is_empty()  # noqa: F841
    user = await get_user_from_session(session)
    request.state.session = session if user.is_authenticated else None
    request.state.user = user if user.is_authenticated else None
    response = await call_next(request)
    return response


application.add_exception_handler(Exception, unhandled_exception_handler)

application.include_router(router)
application.mount("/", get_asgi_application())
